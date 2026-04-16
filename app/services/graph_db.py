import os
from neo4j import GraphDatabase

class GraphDBClient:
    def __init__(self):

        neo4j_uri = os.getenv("NEO4J_URI")
        neo4j_user = os.getenv("NEO4J_USER")
        neo4j_pass = os.getenv("NEO4J_PASS")# 👈 改回 NEO4J_PASS！
        
        # 2. 连接图谱
        self.driver = GraphDatabase.driver(
            neo4j_uri, 
            auth=(neo4j_user, neo4j_pass),
            max_connection_lifetime=200,
            keep_alive=True
        )

    def search_disease_prescription(self, disease_name: str) -> dict:
        """在图谱中提取病害处方"""
        cypher = """
        MATCH (d:Disease {name: $name})
        RETURN d.rag_summary AS summary, 
               d.agricultural AS agricultural, 
               d.biological AS biological, 
               d.chemicals AS chemicals
        """
        with self.driver.session() as session:
            result = session.run(cypher, name=disease_name).single()
            if result:
                return {
                    "summary": result["summary"],
                    "agricultural": result["agricultural"],
                    "biological": result["biological"],
                    "chemicals": result["chemicals"]
                }
            return None

    def add_disease_node(self, disease_name: str, symptom: str, treatment: str):
        """注入新知识节点"""
        cypher = """
        MERGE (d:Disease {name: $disease_name})
        SET d.rag_summary = $symptom + '。防治建议：' + $treatment
        RETURN d
        """
        with self.driver.session() as session:
            session.run(cypher, disease_name=disease_name, symptom=symptom, treatment=treatment)

    def get_visualization_data(self, limit: int = 100, disease_name: str = None) -> dict:
        """获取大屏关系图谱数据"""
        # (这里把咱们刚写好的图谱大屏可视化逻辑挪过来，省略长代码保持清爽，你直接把你 ai_engine 里的贴进来即可)
        pass