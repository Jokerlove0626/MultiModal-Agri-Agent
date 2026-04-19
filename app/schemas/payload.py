from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str
    session_id: str = "default_session"

class KnowledgeAddRequest(BaseModel):
    disease_name: str
    symptom: str
    treatment: str
    admin_token: str

class ChatRequest(BaseModel):
    query: str
    session_id: str = "default_session"
    # 👇 新增地理位置字段，默认是未知
    province: str = "未知" 
    city: str = "未知"