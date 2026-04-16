from fastapi import APIRouter, HTTPException, Request
from app.schemas.payload import KnowledgeAddRequest

router = APIRouter()

@router.post("/add")
async def add_knowledge_endpoint(request: KnowledgeAddRequest, req: Request):
    """知识入库接口"""
    engine = req.app.state.rag_engine
    if not engine:
        raise HTTPException(status_code=500, detail="AI引擎未就绪")
        
    if request.admin_token != "super_joker_2024":
        raise HTTPException(status_code=403, detail="没有权限！")
        
    success = engine.add_new_disease(
        disease_name=request.disease_name,
        symptom=request.symptom,
        treatment=request.treatment
    )
    if success:
        return {"status": "success", "message": f"成功录入【{request.disease_name}】的知识！"}
    else:
        raise HTTPException(status_code=500, detail="知识入库失败，请看控制台日志。")