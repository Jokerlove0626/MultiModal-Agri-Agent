import os
import asyncio
from openai import AsyncOpenAI  
# 👇 极其清晰的引库方式
from app.services.memory import MemoryManager
from app.services.llm_client import LLMClient
from app.services.graph_db import GraphDBClient
from app.services.vector_db import VectorDBClient

import datetime
from app.db.session import SessionLocal # 👈 引入水龙头
from app.db.models import PestRecord   # 👈 引入表模型

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
        """核心文本链路编排 (SSE 流式输出版)"""
        
        # 为了保证 SSE 格式，遇到提前拦截拦截时，我们需要用 yield 吐出文字并结束
        # 1. 拿记忆
        recent_history = self.memory.get_recent_history(session_id)
        is_follow_up = False

        yield "data: 🔍 正在检索图谱与向量知识库...<br>\n\n"
        await asyncio.sleep(0.1)

        # 2. 查向量
        best_score, matched_disease = self.vector_db.search_and_rerank(user_query)
        
        # 👇 新增：让终端把底牌亮出来！你以后在终端就能看到为什么被拦截了
        print(f"🧐 [诊断路由] 用户输入: '{user_query}' | 向量最高得分: {best_score:.2f} | 匹配病害: {matched_disease}")

        # 3. 意图拦截护栏 (咱们在测试期，干脆把门槛降到极低的 0.50！)
        if best_score < 0.50:  
            print("🛑 [拦截护栏] 得分太低，直接拒绝，不调用千问大模型！")
            if source == "vision":
                # ⚠️ 注意：这里我直接在 Python 里把所有的 \n 全换成了 HTML 的 <br>
                msg = f"系统提取到的症状为：【{user_query}】<br><br>⚠️ **知识库未收录**：当前图谱中暂无该病害的详细处方。"
                yield f"data: {msg}\n\n"
                yield "data: [DONE]\n\n"
                return
            elif self.memory.has_history(session_id):
                print("🔄 [意图路由] 检索得分过低，放行至多轮对话！")
                is_follow_up = True
                matched_disease = "上下文追问 (需大模型仲裁)"
            else:
                # ⚠️ 注意：这里也全换成了 <br>，绝对不会再被前端切断了！
                msg = f"系统提取到的症状为：【{user_query}】<br><br>⚠️ **诊断置信度不足 ({best_score:.2f})**：未能匹配到相关病害。"
                yield f"data: {msg}\n\n"
                yield "data: [DONE]\n\n"
                return

        # 4. 查图谱组装提示词
        if is_follow_up:
            system_prompt = """你是一位严谨且亲和的农业植保专家。
【当前状态】：用户正在进行上下文追问。
【最高安全指令】：
1. 请直接结合【历史对话】顺畅、自然地回答用户的问题。
2. 若用户突然询问全新的病害，必须严格回复：“抱歉，当前知识库尚未收录该病害的资料，系统拒绝提供未经验证的处方。”
3. 绝对不要在回复中暴露你的分析过程或提及“系统指令”。”"""
            context_str = "本次提问为上下文追问，无新增参考资料，请完全依赖历史对话作答。"
        else:
            graph_data = self.graph_db.search_disease_prescription(matched_disease)
            if not graph_data:
                msg = f"识别为【{matched_disease}】，但无详细处方。"
                yield f"data: {msg}\n\n"
                yield "data: [DONE]\n\n"
                return
                
            self._log_pest_occurrence(matched_disease, province, city)

            context_str = f"【诊断】: {matched_disease}\n【摘要】: {graph_data['summary']}\n【农业】: {graph_data['agricultural']}\n【生物】: {graph_data['biological']}\n【化学】: {graph_data['chemicals']}"

            system_prompt = """你是一位严谨的农业植保专家。
【最高限制指令】：
1. 优先使用【本次检索资料】与【历史对话】中提供的信息回答问题。
2. 严禁自行补充未在资料中出现的农药建议。
3. 若给出药方，请整理成 Markdown 表格。
4. 绝对不要在回复中暴露你的分析过程。"""

        yield "data: 🧠 检索完毕，千问大模型正在生成诊断报告...<br><br>\n\n"

        # 5. 拼装大模型并呼叫
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(recent_history)
        messages.append({"role": "user", "content": f"用户提问：{user_query}\n\n【本次检索资料】：\n{context_str}"})

# 👇 核心流式处理区
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
                    full_answer += char # 攒字（存进记忆的还是纯净的 \n）
                    
                    # 🚀 终极杀招：直接把大模型的换行替换成网页换行 <br>
                    # 这样既不会破坏 SSE 协议，前端也不会出现奇怪的 data: 了！
                    safe_char = char.replace('\n', '<br>')
                    yield f"data: {safe_char}\n\n"
                    
            # 6. 存记忆 
            self.memory.save_interaction(session_id, user_query, full_answer)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            yield f"data: \n\n⚠️ 大模型连接异常: {str(e)}\n\n"
            
        # 结束推流信号
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

    async def analyze_image_and_answer(self, base64_image: str, crop_name: str = "", user_text: str = "", session_id: str = "default_session") -> dict:
        """核心视觉链路编排"""
        try:
            history_context = "无"
            if self.memory.has_history(session_id):
                recent_msgs = self.memory.get_recent_history(session_id, limit=2)
                history_context = "\n".join([f"{msg['role']}: {msg['content'][:100]}..." for msg in recent_msgs])

            crop_hint = f"已知图片中的作物是【{crop_name}】。" if crop_name else "【重要任务】：请先准确识别图片。"
            user_msg_hint = f"\n【用户随图附言】：{user_text}" if user_text else ""

            sys_prompt = f"""你是一位资深的农业植保专家。
【历史聊天记录】：
{history_context}
{user_msg_hint}

【任务说明】：请仔细观察图片并结合记录诊断。
必须且只能输出单行格式：“[作物名称][你猜测的病害名称] [核心症状描述]”。如果非植物，回复“非植物”。"""

            symptom = await self.llm.chat_vision(sys_prompt, base64_image)

            if "非植物" in symptom:
                return {"status": "error", "message": "图片看起来不像植物，请上传作物病害图片。"}

            final_answer = await self.generate_answer(symptom, session_id=session_id, source="vision")
            return {"status": "success", "extracted_symptom": symptom, "answer": final_answer}
        except Exception as e:
            return {"status": "error", "message": f"视觉模型错误: {str(e)}"}

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

