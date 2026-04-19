import base64
from fastapi import APIRouter, HTTPException, File, UploadFile, Form, Request
from fastapi.responses import StreamingResponse # 👈 极其关键：修复 500 报错的救命稻草
from app.schemas.payload import ChatRequest

router = APIRouter()

# 👇 修复：给流式接口改个独立的名字
@router.post("/stream")
async def chat_stream_endpoint(request: ChatRequest, req: Request):
    """文本问答接口 (流式 SSE 版本)"""
    engine = req.app.state.rag_engine
    if not engine:
        raise HTTPException(status_code=500, detail="AI引擎未就绪")
    
    try:
        # 直接把引擎的流式生成器塞进 StreamingResponse！
        return StreamingResponse(
            engine.generate_answer_stream(request.query, request.session_id,province=request.province, city=request.city),
            media_type="text/event-stream"
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# 👇 保持原名，这是普通的同步接口
@router.post("/")
async def chat_endpoint(request: ChatRequest, req: Request):
    """文本问答接口 (普通同步版本)"""
    engine = req.app.state.rag_engine
    if not engine:
        raise HTTPException(status_code=500, detail="AI引擎未就绪")
    try:
        answer = await engine.generate_answer(request.query, request.session_id)
        return {"status": "success", "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/identify")
async def identify_image_endpoint(
    req: Request,
    file: UploadFile = File(...),
    crop_name: str = Form(""),
    user_text: str = Form(""),
    session_id: str = Form("default_session"),
    province: str = Form("未知"),
    city: str = Form("未知")
):
    """视觉识别与多模态问答接口（流式SSE）"""
    engine = req.app.state.rag_engine
    if not engine:
        raise HTTPException(status_code=500, detail="AI引擎未就绪")
    try:
        contents = await file.read()
        base64_image = base64.b64encode(contents).decode("utf-8")
        # 直接用流式生成器包装
        return StreamingResponse(
            engine.analyze_image_and_answer(
                base64_image=base64_image,
                crop_name=crop_name,
                user_text=user_text,
                session_id=session_id
            ),
            media_type="text/event-stream"
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))