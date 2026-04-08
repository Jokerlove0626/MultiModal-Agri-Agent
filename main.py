import base64
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# 1. 必须在最开头加载 .env
load_dotenv()

# 2. 从我们自己的 services 导入 AI 引擎
from app.services.ai_engine import AgriculturalRAGEngine

app = FastAPI(title="Jokerlove 农业知识引擎 API")

# 3. 初始化引擎实例
try:
    rag_engine = AgriculturalRAGEngine()
except Exception as e:
    print(f"🚨 引擎初始化失败: {e}")
    rag_engine = None

class ChatRequest(BaseModel):
    query: str

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    if not rag_engine:
        raise HTTPException(status_code=500, detail="AI 引擎未就绪，请检查服务端配置")
    try:
        answer = await rag_engine.generate_answer(request.query)
        return {"status": "success", "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/identify")
async def identify_image_endpoint(file: UploadFile = File(...)):
    if not rag_engine:
        raise HTTPException(status_code=500, detail="AI 引擎未就绪")
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="请上传图片文件！")
    
    try:
        contents = await file.read()
        base64_encoded = base64.b64encode(contents).decode("utf-8")
        result = await rag_engine.analyze_image_and_answer(base64_encoded)
        
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result["message"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # 启动服务
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)