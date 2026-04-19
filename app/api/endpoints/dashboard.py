import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.db.models import PestRecord

router = APIRouter()

@router.get("/stats")
async def get_dashboard_stats(days: int = 180, db: Session = Depends(get_db)):
    """真实 MySQL 统计接口：拉取并聚合各省病害数据"""
    
    # 1. 计算时间边界 (例如最近半年)
    start_date = datetime.date.today() - datetime.timedelta(days=days)

    try:
        # 2. 极其丝滑的 SQLAlchemy 聚合查询！
        # 对应 SQL: SELECT province, COUNT(id), GROUP_CONCAT(DISTINCT pest_name) FROM pest_records ...
        stats_query = (
            db.query(
                PestRecord.province,
                func.count(PestRecord.id).label("total_cases"),
                # MySQL 特供绝技：把同一个省份下的不同病害名字，用逗号拼成一个字符串
                func.group_concat(PestRecord.pest_name.distinct()).label("main_pests")
            )
            .filter(PestRecord.report_date >= start_date)
            .group_by(PestRecord.province)
            .all()
        )

        # 3. 组装成 ECharts 需要的字典格式
        result_data = []
        for row in stats_query:
            result_data.append({
                "name": row.province,
                "value": row.total_cases,
                "pests": row.main_pests.split(",") if row.main_pests else []
            })

        return {"status": "success", "data": result_data}

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status": "error", "message": f"数据库查询失败: {str(e)}"}