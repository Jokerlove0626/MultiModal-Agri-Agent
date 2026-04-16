import asyncio
from fastapi import APIRouter, HTTPException, Request

router = APIRouter()

@router.get("/visualize")
async def visualize_graph_endpoint(req: Request, disease_name: str = None, limit: int = 150):
    """大屏可视化：图谱数据提取接口"""
    engine = req.app.state.rag_engine
    if not engine:
        raise HTTPException(status_code=500, detail="AI引擎未就绪")
        
    try:
        graph_data = await asyncio.to_thread(
            engine.get_graph_visualization_data, 
            limit, 
            disease_name
        )
        return {"status": "success", "data": graph_data}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"图谱数据提取失败: {str(e)}")