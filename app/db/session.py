# Database session and engine setup
# Example using SQLAlchemy async:
#
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker
# from app.core.config import settings
#
# engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)
# AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
#
# async def get_db() -> AsyncSession:
#     async with AsyncSessionLocal() as session:
#         yield session


import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. 拿到 .env 里的连接地址
SQLALCHEMY_DATABASE_URL = os.getenv("MYSQL_DATABASE_URL", "mysql+pymysql://root:123456@127.0.0.1:3306/agri_db")

# 2. 创建数据库引擎 (水泵)
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, pool_size=10)

# 3. 创建会话工厂 (水龙头)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. 创建 ORM 基类 (所有表结构的祖师爷)
Base = declarative_base()

# 5. FastAPI 专属的依赖注入函数 (极其重要：确保每次请求用完数据库自动关门)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()