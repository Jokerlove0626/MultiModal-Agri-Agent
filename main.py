import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv


# 👇 1. 导入咱们刚刚重构好的“总机” (注意去掉了 s，变量变成了 api_router)
from app.api.router import api_router
from app.services.orchestrator import RAGOrchestrator


from app.db.session import engine, Base
from app.db import models

import redis.asyncio as redis
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)



# 每次系统启动时，检查 MySQL 里有没有这些表，没有就自动建表！
Base.metadata.create_all(bind=engine)


load_dotenv()

# 👇 2. 保留你极其优秀的生命周期管理机制
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("⏳ 正在唤醒智农大夫核心大脑...")
    # 将实例化后的引擎挂载到 app.state 上，实现全局单例共享！
    app.state.rag_engine = RAGOrchestrator()
    print("✅ 智农大夫核心大脑已全部就绪！")
    yield
    print("🛑 正在关闭系统，释放资源...")

# 👇 3. 初始化应用，挂载 lifespan
app = FastAPI(
    title="智农大夫微服务引擎",
    description="基于 Graph RAG 的农业病害诊断专家系统",
    version="1.0.0",
    lifespan=lifespan
)

# 👇 4. 保留跨域配置（未来对接前端 Vue/React 极其关键）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 👇 5. 🚀 挂载全新总机，无需在底层端点写前缀，在这里统一接管！
app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    # 建议 host 改为 0.0.0.0，方便以后局域网手机测试或者 Docker 部署
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)