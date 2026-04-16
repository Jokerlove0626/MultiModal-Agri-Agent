import os
import chromadb
from chromadb.utils import embedding_functions
from neo4j import GraphDatabase
from openai import AsyncOpenAI
from sentence_transformers import CrossEncoder
import numpy as np

class AgriculturalRAGEngine:
    def __init__(self):
        # 1. 自动从环境变量加载配置
        neo4j_uri = os.getenv("NEO4J_URI")
        neo4j_user = os.getenv("NEO4J_USER")
        neo4j_pass = os.getenv("NEO4J_PASS")
        chroma_path = os.getenv("CHROMA_PATH", "./data/chroma_db")
        dashscope_key = os.getenv("DASHSCOPE_API_KEY")

        if not all([neo4j_uri, neo4j_user, neo4j_pass, dashscope_key]):
            raise ValueError("🚨 环境变量缺失，请检查根目录下的 .env 文件！")

        # 2. 挂载数据库
        self.neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_pass),max_connection_lifetime=200,keep_alive=True)
        self.chroma_client = chromadb.PersistentClient(path=chroma_path)
        self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="BAAI/bge-large-zh-v1.5")
        self.collection = self.chroma_client.get_collection(name="agriculture_kg", embedding_function=self.ef)
        
        # 3. 挂载重排模型 (Reranker)
        print("🧠 正在加载 Rerank 重排模型 (首次启动会下载，请稍候)...")
        self.reranker = CrossEncoder('BAAI/bge-reranker-base')
        print("✅ 重排模型加载完毕！")

        # 4. 挂载阿里 Qwen 大模型
        self.llm_client = AsyncOpenAI(
            api_key=dashscope_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )

        # 5.👇 新增：初始化一个字典作为内存中的“海马体”记忆库
        self.chat_history = {}

    def _search_graph(self, disease_name):
        """精准提取图谱处方"""
        cypher = """
        MATCH (d:Disease {name: $disease_name})
        OPTIONAL MATCH (d)-[rc:CHEMICAL_CONTROL]->(m:Medicine)
        WITH d, collect(DISTINCT {name: m.name, dosage: rc.dosage, timing: rc.timing}) AS chemicals
        OPTIONAL MATCH (d)-[ra:AGRICULTURAL_CONTROL]->(am:Method)
        WITH d, chemicals, collect(DISTINCT am.name) AS agricultural
        OPTIONAL MATCH (d)-[rb:BIOLOGICAL_CONTROL]->(b:BiologicalAgent)
        WITH d, chemicals, agricultural, collect(DISTINCT {name: b.name, detail: rb.detail}) AS biological
        RETURN d.rag_summary AS summary, chemicals, agricultural, biological
        """
        # 指定 database="neo4j" 避免 MissingDatabaseError
        with self.neo4j_driver.session(database="fe1ff8d4") as session:
            result = session.run(cypher, disease_name=disease_name).single()
            if not result: return None
            return {
                "summary": result["summary"],
                "chemicals": result["chemicals"],
                "agricultural": result["agricultural"],
                "biological": result["biological"]
            }

    async def generate_answer(self, user_query: str, session_id: str = "default_session", source: str = "text") -> str:
        """文本 RAG 业务 (带意图路由 + Rerank重排 + 多轮记忆滑动窗口)"""
        
        # 1. 为新用户开辟记忆阵列
        if session_id not in self.chat_history:
            self.chat_history[session_id] = []

        is_follow_up = False

        # 【阶段 1 & 2：检索与精排】
        vector_res = self.collection.query(query_texts=[user_query], n_results=15)
        
        if not vector_res['metadatas'][0]:
            best_score = 0
            matched_disease = "无"
        else:
            candidate_diseases = [meta['disease_name'] for meta in vector_res['metadatas'][0]]
            candidate_docs = vector_res['documents'][0]  
            
            pairs = [[user_query, doc] for doc in candidate_docs]
            scores = self.reranker.predict(pairs)
            
            best_index = np.argmax(scores)
            matched_disease = candidate_diseases[best_index]
            best_score = scores[best_index]

            print(f"🎯 [检索分析] 粗排候选: {candidate_diseases}")
            print(f"🎯 [检索分析] 重排最高分命中: {matched_disease} (得分: {best_score:.4f})")
        
        # 【核心升级：双重意图路由防御体系】
        if best_score < 0.80:
            if source == "vision":
                # 护栏一：如果是新传的图片，但分很低，直接判定为【库中无此病害】！
                return f"系统提取到的症状为：【{user_query}】\n\n⚠️ **知识库未收录**：当前图谱中暂无该病害的详细处方。请您调用【人工知识注入接口】补充该数据后再次尝试！"
            elif len(self.chat_history[session_id]) > 0:
                # 护栏二：打字追问防偏航
                print("🔄 [意图路由] 检索得分过低，放行至多轮对话，交由大模型进行 OOD 仲裁！")
                is_follow_up = True
            else:
                return f"系统提取到的症状为：【{user_query}】。\n\n⚠️ **诊断置信度不足 ({best_score:.2f})**：未能匹配到相关病害。"

 # 【阶段 3：图谱穿透与数据组装】
        if is_follow_up:
            # 💡 追问模式：系统指令归系统，用户提问归用户
            system_prompt = """你是一位严谨且亲和的农业植保专家。
【当前状态】：用户正在进行上下文追问。
【最高安全指令】：
1. 请直接结合【历史对话】顺畅、自然地回答用户的问题。
2. 若用户突然询问一种【全新的、历史记录中从未出现过的病害或作物】，必须严格回复：“抱歉，当前知识库尚未收录该病害的资料，为保证农业用药安全，系统拒绝提供未经验证的处方。请通过管理员后台补充该知识。”
3. 绝对不要在回复中暴露你的分析过程、判定依据或提及“系统指令”等字眼，直接给出最终的专业回复即可。"""
            
            context_str = "本次提问为上下文追问，无新增参考资料，请完全依赖历史对话作答。"
        else:
            # 💡 首问模式：去图谱里拿药方
            graph_data = self._search_graph(matched_disease)
            if not graph_data:
                return f"识别为【{matched_disease}】，但无详细处方。"
            context_str = f"【诊断】: {matched_disease}\n【摘要】: {graph_data['summary']}\n【农业】: {graph_data['agricultural']}\n【生物】: {graph_data['biological']}\n【化学】: {graph_data['chemicals']}"
            
            system_prompt = """你是一位严谨的农业植保专家。
【最高限制指令】：
1. 优先使用【本次检索资料】与【历史对话】中提供的信息回答问题。
2. 严禁自行补充任何未在资料中出现的病害特征或农药建议。
3. 若给出药方，请整理成 Markdown 表格。
4. 绝对不要在回复中暴露你的分析过程或提及“系统指令”。"""
        
        # 4. 🧠 记忆缝合：角色界限极其分明
        # 把所有的“紧箍咒”全放进 system 角色里
        messages = [{"role": "system", "content": system_prompt}]  
        
        recent_history = self.chat_history[session_id][-4:]
        messages.extend(recent_history)
        
        # 用户的提问现在极其干净，只包含单纯的问题和单纯的资料
        current_user_content = f"用户提问：{user_query}\n\n【本次检索资料】：\n{context_str}"
        messages.append({"role": "user", "content": current_user_content})

        # 5. 呼叫大模型
        response = await self.llm_client.chat.completions.create(
            model="qwen-plus", 
            messages=messages,
            temperature=0.3 
        )

        answer = response.choices[0].message.content

        # 6. 🔄 记忆飞轮更新
        self.chat_history[session_id].append({"role": "user", "content": user_query})
        self.chat_history[session_id].append({"role": "assistant", "content": answer})

        return answer


# 👇 1. 签名新增 session_id 和 user_text（用户随图片附带的一句话）
    async def analyze_image_and_answer(self, base64_image: str, crop_name: str = "", user_text: str = "", session_id: str = "default_session") -> dict:
        """视觉 RAG 业务 (带上下文记忆的多模态提取)"""
        try:
            # 2. 🧠 提取最近的记忆（作为前情提要）
            history_context = "无"
            if session_id in self.chat_history and len(self.chat_history[session_id]) > 0:
                # 只取最近的两句对话，防止干扰
                recent_msgs = self.chat_history[session_id][-2:]
                history_context = "\n".join([f"{msg['role']}: {msg['content'][:100]}..." for msg in recent_msgs])

            crop_hint = f"已知图片中的作物是【{crop_name}】。" if crop_name else "【重要任务】：请先准确识别图片中的作物种类。"
            user_msg_hint = f"\n【用户随图附言】：{user_text}" if user_text else ""
            
            # 3. 📝 组装具有“上帝视角”的视觉 Prompt
            sys_prompt = f"""你是一位资深的农业植保专家。
【历史聊天记录】：
{history_context}
{user_msg_hint}

【任务说明】：
请仔细观察用户刚刚上传的最新图片，并结合上述【历史聊天记录】和【附言】进行诊断。
为了配合底层的 GraphRAG 知识库检索，你必须且只能输出严格的【单行格式】：
“[作物名称][你猜测的病害名称] [图片中的核心症状描述]”

【特殊指令】：
即使你结合上下文发现这是上一轮讨论过的病害，也必须在单行格式中明确写出病害名称和最新的症状，作为检索锚点。
绝对不要输出任何多余的问候语、解释或换行。如果图片根本不是植物，请直接回复“非植物”。"""

            vision_response = await self.llm_client.chat.completions.create(
                model="qwen-vl-max",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": sys_prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }
                ]
            )
            symptom = vision_response.choices[0].message.content.strip()
            
            if "非植物" in symptom:
                return {"status": "error", "message": "图片看起来不像植物，请上传作物病害图片。"}
            
            print(f"👁️ [视觉感知-记忆融合] 提取的重排检索词: {symptom}")
            
            # 4. 🔗 把提取出的超级锚点，连同 session_id 一起交给下游的文本 RAG 引擎
            # 注意：虽然是图片，但因为融入了历史记忆，我们可以把它当成一次带强烈背景信息的查询
            final_answer = await self.generate_answer(symptom, session_id=session_id, source="vision")
            
            return {"status": "success", "extracted_symptom": symptom, "answer": final_answer}
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {"status": "error", "message": f"视觉模型错误: {str(e)}"}


    async def add_new_disease(self, disease_name: str, symptom: str, treatment: str) -> bool:
        """动态知识注入：同时更新图谱与向量库"""
        try:
            print(f"📥 [知识注入] 正在学习新病害: {disease_name}...")
            
            # 1. 写入 ChromaDB (让系统未来能“检索”到它)
            # 以病害名作为唯一 ID，如果存在会自动覆盖 (Upsert)
            document_text = f"【病害名称】: {disease_name}\n【症状描述】: {symptom}\n【防治方案】: {treatment}"
            self.collection.upsert(
                documents=[document_text],
                metadatas=[{"disease_name": disease_name}],
                ids=[f"disease_{disease_name}"]
            )
            
            # 2. 写入 Neo4j (让系统未来能“提取”出处方)
            # 使用 MERGE 保证节点唯一性，并直接把所有信息塞进 rag_summary
            # (如果你有更复杂的实体关系，可以在这里扩写 Cypher)
            cypher = """
            MERGE (d:Disease {name: $disease_name})
            SET d.rag_summary = $symptom + '。防治建议：' + $treatment
            RETURN d
            """
            # 注意：如果之前遇到 databaseNotFound 报错，这里也同样保持 () 留空
            with self.neo4j_driver.session() as session:
                session.run(cypher, disease_name=disease_name, symptom=symptom, treatment=treatment)
                
            print(f"✅ [知识注入] 学习完成！知识库已更新。")
            return True
        except Exception as e:
            print(f"🚨 [知识注入失败]: {e}")
            return False

    def get_graph_visualization_data(self, limit: int = 100, disease_name: str = None) -> dict:
        """提取图谱数据供前端可视化 (转为标准的 Nodes & Edges 格式)"""
        nodes_dict = {}
        edges_list = []
        
        # 动态构建 Cypher 语句：如果传了病害名，就查这个病的局部图谱；如果不传，就查全局图谱
        if disease_name:
            cypher = """
            MATCH (n:Disease {name: $disease_name})-[r]-(m)
            RETURN n, r, m
            """
            params = {"disease_name": disease_name}
        else:
            cypher = """
            MATCH (n)-[r]->(m)
            RETURN n, r, m LIMIT $limit
            """
            params = {"limit": limit}

        try:
            # 注意：这个方法是同步的，所以直接用 with session 即可
            with self.neo4j_driver.session() as session:
                results = session.run(cypher, **params)
                
                for record in results:
                    n = record["n"]
                    m = record["m"]
                    r = record["r"]

                    # 1. 解析起点节点 (Node)
                    n_id = str(getattr(n, 'element_id', getattr(n, 'id', n.get('name'))))
                    n_label = list(n.labels)[0] if n.labels else "Unknown"
                    if n_id not in nodes_dict:
                        nodes_dict[n_id] = {
                            "id": n_id,
                            "name": n.get("name", "未命名节点"),
                            "category": n_label
                        }

                    # 2. 解析终点节点 (Node)
                    m_id = str(getattr(m, 'element_id', getattr(m, 'id', m.get('name'))))
                    m_label = list(m.labels)[0] if m.labels else "Unknown"
                    if m_id not in nodes_dict:
                        nodes_dict[m_id] = {
                            "id": m_id,
                            "name": m.get("name", "未命名节点"),
                            "category": m_label
                        }

                    # 3. 解析连线关系 (Edge)
                    edges_list.append({
                        "source": n_id,
                        "target": m_id,
                        "label": r.type
                    })

            return {
                "nodes": list(nodes_dict.values()),
                "edges": edges_list
            }
            
        except Exception as e:
            print(f"🚨 [图谱可视化提取失败]: {e}")
            return {"nodes": [], "edges": []}