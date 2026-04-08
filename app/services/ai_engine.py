import os
import chromadb
from chromadb.utils import embedding_functions
from neo4j import GraphDatabase
from openai import AsyncOpenAI

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
        self.neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_pass))
        self.chroma_client = chromadb.PersistentClient(path=chroma_path)
        self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="BAAI/bge-large-zh-v1.5")
        self.collection = self.chroma_client.get_collection(name="agriculture_kg", embedding_function=self.ef)
        
        # 3. 挂载阿里 Qwen 大模型
        self.llm_client = AsyncOpenAI(
            api_key=dashscope_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )

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
        with self.neo4j_driver.session() as session:
            result = session.run(cypher, disease_name=disease_name).single()
            if not result: return None
            return {
                "summary": result["summary"],
                "chemicals": result["chemicals"],
                "agricultural": result["agricultural"],
                "biological": result["biological"]
            }

    async def generate_answer(self, user_query: str) -> str:
        """文本 RAG 业务"""
        vector_res = self.collection.query(query_texts=[user_query], n_results=1)
        if not vector_res['metadatas'][0]:
            return "抱歉，知识库中暂未找到相关病害。"
            
        matched_disease = vector_res['metadatas'][0][0]['disease_name']
        graph_data = self._search_graph(matched_disease)
        
        if not graph_data:
            return f"识别为【{matched_disease}】，但无详细处方。"
            
        system_prompt = "你是一位资深农业植保专家，请根据图谱数据用亲和的语气回答。务必保留药剂的浓度和使用时机。"
        context_str = f"【诊断】: {matched_disease}\n【摘要】: {graph_data['summary']}\n【农业】: {graph_data['agricultural']}\n【生物】: {graph_data['biological']}\n【化学】: {graph_data['chemicals']}"
        
        response = await self.llm_client.chat.completions.create(
            model="qwen-plus", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"用户提问：{user_query}\n\n参考资料：\n{context_str}"}
            ],
            temperature=0.3 
        )
        return response.choices[0].message.content

    async def analyze_image_and_answer(self, base64_image: str) -> dict:
        """视觉 RAG 业务"""
        try:
            vision_response = await self.llm_client.chat.completions.create(
                model="qwen3.6-plus",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "你是一个农业病害诊断专家。描述图中作物的异常症状（如斑点颜色、叶片卷曲等）。只描述症状，不瞎猜病名。如果不是植物回复‘非植物’。"},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }
                ]
            )
            symptom = vision_response.choices[0].message.content
            
            if "非植物" in symptom:
                return {"status": "error", "message": "图片看起来不像植物，请上传作物病害图片。"}
            
            final_answer = await self.generate_answer(symptom)
            return {"status": "success", "extracted_symptom": symptom, "answer": final_answer}
            
        except Exception as e:
            return {"status": "error", "message": f"视觉模型错误: {str(e)}"}