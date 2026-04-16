from fastapi import APIRouter
from app.api.endpoints import chat, knowledge, graph

# 建立总机
api_router = APIRouter()

# 挂载分机：注意这里的 prefix 决定了最终的 URL
api_router.include_router(chat.router, prefix="/chat", tags=["🤖 智能问答与视觉诊断"])
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["📚 知识库后台管理"])
api_router.include_router(graph.router, prefix="/graph", tags=["🕸️ 知识图谱大屏分析"])