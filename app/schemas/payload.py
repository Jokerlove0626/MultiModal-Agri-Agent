from pydantic import BaseModel

class ChatRequest(BaseModel):
    query: str
    session_id: str = "default_session"

class KnowledgeAddRequest(BaseModel):
    disease_name: str
    symptom: str
    treatment: str
    admin_token: str