import os
import chromadb
import numpy as np
from chromadb.utils import embedding_functions
# 👇 极其优雅：直接使用自带的成熟库，彻底告别依赖冲突！
from sentence_transformers import CrossEncoder

class VectorDBClient:
    def __init__(self):
        # 初始化向量库
        # 获取项目根目录
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) 
        # 👇 优雅地指向 data/chroma_db
        chroma_path = os.path.join(base_dir, "data", "chroma_db")
        
        self.chroma_client = chromadb.PersistentClient(path=chroma_path)
        self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="BAAI/bge-large-zh-v1.5")
        self.collection = self.chroma_client.get_or_create_collection(name="disease_symptoms", embedding_function=self.ef)
        
        # 👇 替换重排模型：用 CrossEncoder 完美平替 FlagReranker
        print("⏳ 正在加载交叉重排大模型 (Cross-Encoder)...")
        self.reranker = CrossEncoder('BAAI/bge-reranker-large', max_length=512)

    def search_and_rerank(self, query: str, top_k: int = 15) -> tuple:
        """检索并返回重排后的最高分和病名"""
        vector_res = self.collection.query(query_texts=[query], n_results=top_k)
        
        if not vector_res['metadatas'][0]:
            return 0.0, "无"

        candidate_diseases = [meta['disease_name'] for meta in vector_res['metadatas'][0]]
        candidate_docs = vector_res['documents'][0]  
        
        # Rerank 精排 (API 完美兼容！)
        pairs = [[query, doc] for doc in candidate_docs]
        scores = self.reranker.predict(pairs)
        
        best_index = np.argmax(scores)
        
        # 将 numpy 的 float32 转为标准 python float，防止后续报错
        best_score = float(scores[best_index]) 
        
        return best_score, candidate_diseases[best_index]

    def add_knowledge_vector(self, disease_name: str, symptom: str, treatment: str):
        """注入新知识向量"""
        document_text = f"【病害名称】: {disease_name}\n【症状描述】: {symptom}\n【防治方案】: {treatment}"
        self.collection.upsert(
            documents=[document_text],
            metadatas=[{"disease_name": disease_name}],
            ids=[f"disease_{disease_name}"]
        )