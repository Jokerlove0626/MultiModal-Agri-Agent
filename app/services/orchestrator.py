import os
import asyncio
from openai import AsyncOpenAI  
# 👇 极其清晰的引库方式
from app.services.memory import MemoryManager
from app.services.llm_client import LLMClient
from app.services.graph_db import GraphDBClient
from app.services.vector_db import VectorDBClient
import json
import datetime
from app.db.session import SessionLocal # 👈 引入水龙头
from app.db.models import PestRecord   # 👈 引入表模型

import asyncio
import hashlib
import redis.asyncio as redis
redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)

class RAGOrchestrator:
    def __init__(self):
        print("⏳ 正在唤醒四大底层兵种...")
        self.memory = MemoryManager()
        self.llm = LLMClient()
        self.graph_db = GraphDBClient()
        self.vector_db = VectorDBClient()
        print("✅ 四大兵种集结完毕！引擎启动！")

    # 👇 新增：千问流式专用客户端 (直接对接阿里云兼容模式)
        api_key = os.getenv("DASHSCOPE_API_KEY")
        if api_key:
            self.stream_llm_client = AsyncOpenAI(
                api_key=api_key,
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
            )
        else:
            print("⚠️ 警告：未检测到 DASHSCOPE_API_KEY，流式输出可能失败！")
    async def generate_answer_stream(self, user_query: str, session_id: str = "default_session", source: str = "text", province: str = "未知", city: str = "未知"):
        """核心文本链路编排 (SSE 流式输出版 + Redis 极速缓存 + 专家诊断版)"""
        
        # 1. 🔑 准备缓存 Key (必须放在最前面)
        query_hash = hashlib.md5(user_query.strip().encode('utf-8')).hexdigest()
        cache_key = f"qa_cache:{query_hash}"

        # 2. ⚡ Redis 极速拦截逻辑
        try:
            cached_answer = await redis_client.get(cache_key)
            if cached_answer:
                print(f"⚡ [Redis 缓存命中] 极速返回: {user_query}")
                yield "data: ⚡ **[极速响应模式]** 命中历史诊断缓存...<br><br>\n\n"
                
                chunk_size = 5
                for i in range(0, len(cached_answer), chunk_size):
                    chunk = cached_answer[i:i+chunk_size]
                    safe_chunk = chunk.replace('\n', '<br>')
                    yield f"data: {safe_chunk}\n\n"
                    await asyncio.sleep(0.01)
                
                yield "data: [DONE]\n\n"
                return 
        except Exception as e:
            print(f"⚠️ Redis 缓存读取失败: {e}")

        # 3. 🔍 检索逻辑 (常规链路)
        recent_history = self.memory.get_recent_history(session_id)
        is_follow_up = False

        yield "data: 🔍 正在检索图谱与向量知识库...<br>\n\n"
        await asyncio.sleep(0.1)

        best_score, matched_disease = self.vector_db.search_and_rerank(user_query)
        
        # 4. 路由拦截与提词组装
        if best_score < 0.50:  
            # ... (此处省略你的得分过低拦截逻辑，保持你原来的即可) ...
            msg = f"⚠️ **诊断置信度不足 ({best_score:.2f})**"
            yield f"data: {msg}\n\n"
            yield "data: [DONE]\n\n"
            return

        # 获取图谱数据
        graph_data = self.graph_db.search_disease_prescription(matched_disease)
        if not graph_data:
            yield f"data: 识别为【{matched_disease}】，但无详细处方。\n\n"
            yield "data: [DONE]\n\n"
            return
            
        self._log_pest_occurrence(matched_disease, province, city)

        # 组装上下文
        context_str = f"【诊断】: {matched_disease}\n【摘要】: {graph_data['summary']}\n【农业】: {graph_data['agricultural']}\n【生物】: {graph_data['biological']}\n【化学】: {graph_data['chemicals']}"

        # 🌟 专家级 System Prompt (注意保持这里的缩进)
        system_prompt = f"""你是一位享誉业内的【首席农业植保专家】。
你现在正在为农户开具一份正式的《植物病虫害专家诊断处方报告》。

[处方报告标准格式]：
# 🛡️ 专家诊断处方单

### 📍 1. 诊断结论
- **确诊对象**：{matched_disease}
- **核心判定**：(根据资料简述该病害威胁)

### 🔍 2. 症状溯源
(基于资料，简要分析特征)

### 💊 3. 综合防治集成方案
---
#### (1) 基础农业措施
* (列出要点)

#### (2) 精准化学干预
| 药剂名称 | 推荐浓度 | 施药时机 | 作用目标 |
| :--- | :--- | :--- | :--- |
| (药剂) | (浓度) | (时机) | (防效) |

### ⚠️ 4. 专家风险提示
- (提示安全与监测要点)

---
(专家鼓励语)"""

        yield "data: 🧠 检索完毕，千问大模型正在生成诊断报告...<br><br>\n\n"

        # 5. 呼叫大模型
        messages = [
            {"role": "system", "content": system_prompt},
            *recent_history,
            {"role": "user", "content": f"用户提问：{user_query}\n\n【资料】：{context_str}"}
        ]

        full_answer = "" 
        try:
            response = await self.stream_llm_client.chat.completions.create(
                model="qwen-plus", 
                messages=messages,
                stream=True,
                temperature=0.1
            )
            async for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    char = chunk.choices[0].delta.content
                    full_answer += char 
                    safe_char = char.replace('\n', '<br>')
                    yield f"data: {safe_char}\n\n"

            
            # 6. 写入记忆与 Redis 缓存
            self.memory.save_interaction(session_id, user_query, full_answer)
            if full_answer:
                try:
                    await redis_client.set(cache_key, full_answer, ex=86400)
                    print(f"💾 [Redis 缓存写入成功] Key: {cache_key}")
                except Exception as cache_err:
                    print(f"⚠️ Redis 写入失败: {cache_err}")

        except Exception as e:
            yield f"data: ⚠️ 大模型异常: {str(e)}\n\n"
            
        # 🏁 最终结束信号 (必须独立一行)
        yield "data: [DONE]\n\n"


    async def generate_answer(self, user_query: str, session_id: str = "default_session", source: str = "text",province: str = "未知", city: str = "未知") -> str:
        """核心文本链路编排"""
        # 1. 拿记忆
        recent_history = self.memory.get_recent_history(session_id)
        is_follow_up = False

        # 2. 查向量
        best_score, matched_disease = self.vector_db.search_and_rerank(user_query)

        # 3. 意图拦截护栏
        if best_score < 0.80:
            if source == "vision":
                return f"系统提取到的症状为：【{user_query}】\n\n⚠️ **知识库未收录**：当前图谱中暂无该病害的详细处方。请补充该数据后再次尝试！"
            elif self.memory.has_history(session_id):
                print("🔄 [意图路由] 检索得分过低，放行至多轮对话！")
                is_follow_up = True
                matched_disease = "上下文追问 (需大模型仲裁)"
            else:
                return f"系统提取到的症状为：【{user_query}】。\n\n⚠️ **诊断置信度不足 ({best_score:.2f})**：未能匹配到相关病害。"

        # 4. 查图谱组装提示词
        if is_follow_up:
            system_prompt = """你是一位严谨且亲和的农业植保专家。
【当前状态】：用户正在进行上下文追问。
【最高安全指令】：
1. 请直接结合【历史对话】顺畅、自然地回答用户的问题。
2. 若用户突然询问全新的病害，必须严格回复：“抱歉，当前知识库尚未收录该病害的资料，系统拒绝提供未经验证的处方。”
3. 绝对不要在回复中暴露你的分析过程或提及“系统指令”。"""
            context_str = "本次提问为上下文追问，无新增参考资料，请完全依赖历史对话作答。"
        else:
            graph_data = self.graph_db.search_disease_prescription(matched_disease)
            if not graph_data:
                return f"识别为【{matched_disease}】，但无详细处方。"
            context_str = f"【诊断】: {matched_disease}\n【摘要】: {graph_data['summary']}\n【农业】: {graph_data['agricultural']}\n【生物】: {graph_data['biological']}\n【化学】: {graph_data['chemicals']}"

            self._log_pest_occurrence(matched_disease, province, city)

            system_prompt = """你是一位严谨的农业植保专家。
【最高限制指令】：
1. 优先使用【本次检索资料】与【历史对话】中提供的信息回答问题。
2. 严禁自行补充未在资料中出现的农药建议。
3. 若给出药方，请整理成 Markdown 表格。
4. 绝对不要在回复中暴露你的分析过程。"""

        # 5. 拼装大模型并呼叫
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(recent_history)
        messages.append({"role": "user", "content": f"用户提问：{user_query}\n\n【本次检索资料】：\n{context_str}"})

        answer = await self.llm.chat_text(messages)

        # 6. 存记忆
        self.memory.save_interaction(session_id, user_query, answer)
        return answer


    async def analyze_image_and_answer(
        self, 
        base64_image: str, 
        crop_name: str = "", 
        user_text: str = "", 
        session_id: str = "default_session",
        province: str = "未知",  
        city: str = "未知"       
    ):
        """核心多模态视觉链路编排（纯文本 SSE 流式，无 JSON 包装）"""
        try:
            history_context = "无"
            if self.memory.has_history(session_id):
                recent_msgs = self.memory.get_recent_history(session_id, limit=2)
                history_context = "\n".join([f"{msg['role']}: {msg['content'][:100]}..." for msg in recent_msgs])

            crop_hint = f"已知图片中的作物是【{crop_name}】。" if crop_name else "【重要任务】：请先准确识别图片。"
            user_msg_hint = f"\n【用户随图附言】：{user_text}" if user_text else ""

            sys_prompt = f"""你是一个运行在后台的农业植保特征提取引擎。
【历史聊天记录】：
{history_context}
{user_msg_hint}
{crop_hint}

【任务说明】：结合记录和图片，精准识别作物种类和病灶特征。
为了配合下游图谱检索，你必须且只能输出【纯文本检索词】。

【强制输出格式】：
单行文本：作物名称 病害名称(若能确定) 核心症状描述
（示例：水稻 纹枯病 叶片出现不规则褐色斑块边缘模糊）

【严格禁令】：
禁止输出任何分析过程、问候语、标点符号或换行符。如果非植物，仅输出“非植物”。"""

            # 1. 纯文本状态提示：直接以 data: 开头
            yield f'data: 👀 正在仔细观察植物叶片...\n\n'

            symptom = ""
            async for delta in self.llm.chat_vision_stream(sys_prompt, base64_image):
                symptom += delta
                # 依然保持沉默，不把提取的废话吐给前端

            if "非植物" in symptom:
                yield f'data: ❌ 图片看起来不像植物，请上传作物病害图片。\n\n'
                return

            # 2. 视觉分析完成，过渡提示
            yield f'data: 🔍 症状提取完毕，正在匹配全国知识图谱...\n\n'

            # 3. 🚀 极其关键：直接透传底层 RAG 引擎的原生数据流
            # 因为 generate_answer_stream 自己已经包装了 "data: xxx \n\n"，所以直接 yield 即可！
            async for chunk in self.generate_answer_stream(
                user_query=symptom,       
                session_id=session_id, 
                source="vision",          
                province=province,        
                city=city                 
            ):
                yield chunk

            # 4. 结束标志（如果你前端是用 [DONE] 来判断结束的话）
            yield f'data: [DONE]\n\n'
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            yield f'data: ❌ 诊断引擎异常: {str(e)}\n\n'

    def add_new_disease(self, disease_name: str, symptom: str, treatment: str) -> bool:
        """知识入库双写编排"""
        try:
            self.vector_db.add_knowledge_vector(disease_name, symptom, treatment)
            self.graph_db.add_disease_node(disease_name, symptom, treatment)
            return True
        except Exception as e:
            print(f"🚨 [知识注入失败]: {e}")
            return False

    def get_graph_visualization_data(self, limit=150, disease_name=None):
        """
        图谱大屏可视化数据提取引擎
        将 Neo4j 里的扁平节点，动态渲染为大屏需要的 Nodes 和 Links 格式
        """
        # 1. 动态拼接 Cypher 查询语句
        cypher = "MATCH (d:Disease) "
        params = {"limit": limit}
        
        if disease_name:
            cypher += "WHERE d.name CONTAINS $disease_name "
            params["disease_name"] = disease_name
            
        cypher += "RETURN d LIMIT $limit"

        # 2. 准备符合前端大屏标准的数据结构
        graph_data = {
            "nodes": [],
            "links": []
        }
        
        # 为了防止节点 ID 冲突，用一个 Set 记录已经处理过的农作物
        processed_crops = set()

        try:
            # 请确认这里的 driver 调用路径是否符合你的代码结构
            # 如果在 Orchestrator 里，可能是 self.graph_db.driver
            with self.graph_db.driver.session() as session:
                results = session.run(cypher, **params)
                
                for record in results:
                    node = record["d"]
                    disease_id = f"disease_{node.id}"
                    disease_title = node.get("name", "未知病害")
                    crop_name = node.get("crop", "未知作物")
                    
                    # --- 添加【病害】节点 ---
                    graph_data["nodes"].append({
                        "id": disease_id,
                        "name": disease_title,
                        "category": "病害",
                        "symbolSize": 50, # 给前端大屏用的节点大小
                        # 把具体的药剂信息塞进 detail 里，方便前端点击展示
                        "detail": {
                            "summary": node.get("rag_summary", ""),
                            "chemical": node.get("chemicals", ""),
                            "biological": node.get("biological", "")
                        }
                    })
                    
                    # --- 添加【农作物】节点 (动态生成中心枢纽) ---
                    crop_id = f"crop_{crop_name}"
                    if crop_name not in processed_crops:
                        graph_data["nodes"].append({
                            "id": crop_id,
                            "name": crop_name,
                            "category": "农作物",
                            "symbolSize": 80 # 作物节点大一点，作为中心
                        })
                        processed_crops.add(crop_name)
                        
                    # --- 添加【连线】 (病害 -> 属于 -> 农作物) ---
                    graph_data["links"].append({
                        "source": disease_id,
                        "target": crop_id,
                        "label": "属于"
                    })

            print(f"🕸️ 成功提取到 {len(graph_data['nodes'])} 个节点, {len(graph_data['links'])} 条关系连线。")
            
            # 👇 极其重要：千万不能忘了 return！
            return graph_data 

        except Exception as e:
            print(f"❌ 提取图谱可视化数据失败: {e}")
            import traceback
            traceback.print_exc()
            # 如果报错，也坚决不能返回 null，返回一个空的规范结构
            return {"nodes": [], "links": []}

    def _log_pest_occurrence(self, disease_name: str, province: str, city: str):
        """静默埋点：将确诊的病害写入 MySQL，供大屏统计"""
        # 如果是无效地点或无效病害，就不记录（防止脏数据污染大屏）
        if province == "未知" or "追问" in disease_name or "未知" in disease_name:
            return

        # 极其规范的数据库操作：随用随开，用完即焚
        db = SessionLocal()
        try:
            record = PestRecord(
                province=province,
                city=city,
                pest_name=disease_name,
                report_date=datetime.date.today(),
                severity=3 # 默认严重程度，或者你可以让 LLM 动态打分
            )
            db.add(record)
            db.commit() # 提交入库！
            print(f"📍 [大屏埋点成功] 记录到 {province}{city} 发生 {disease_name}")
        except Exception as e:
            db.rollback()
            print(f"🚨 [大屏埋点失败] {e}")
        finally:
            db.close() # 极其关键：归还连接，防止连接池爆炸

