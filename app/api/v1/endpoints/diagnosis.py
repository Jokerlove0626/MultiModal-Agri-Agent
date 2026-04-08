import os
import shutil
from fastapi import APIRouter, HTTPException, UploadFile, File
from app.schemas.agriculture import DiagnosisResponse
from app.services import graph_service

# 引入两个引擎函数：一个负责看图，一个负责写报告
from app.services.ai_engine import analyze_image_with_gemini, generate_comprehensive_report

router = APIRouter()

@router.post("/process", response_model=DiagnosisResponse)
async def process_image(file: UploadFile = File(...)) -> DiagnosisResponse:
    # 1. 基础校验
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        raise HTTPException(status_code=400, detail="请上传正确的图片格式 (jpg/png/webp)")

    temp_file_path = f"temp_{file.filename}"
    
    try:
        # 2. 保存临时图片
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 3. 🚀 [阶段一] 视觉大脑：识别出中文病害名
        chinese_pest_name = await analyze_image_with_gemini(temp_file_path)
        
        # 4. 🚀 [阶段二] 图谱检索：查找药方
        pest_info = await graph_service.get_pest_treatments(chinese_pest_name)
        
        # 5. 🚀 [阶段三] 文案大脑：生成最终的中文诊断报告
        expert_report = await generate_comprehensive_report(chinese_pest_name, pest_info)

        # --- 核心修复：手动将数据库对象转换为 Schema 期待的格式 ---
        formatted_treatment = None
        if pest_info and pest_info.treatments:
            # 我们取数据库返回的第一个推荐药方
            first_med = pest_info.treatments[0]
            formatted_treatment = {
                "medicine": first_med.name,             # 对应 Schema 里的 medicine
                "dosage": first_med.dosage or "见包装说明", # 对应 dosage
                "warnings": [first_med.description] if first_med.description else [] # 将描述转为列表
            }

        # 6. ✅ 最终返回：现在数据格式完美契合，不会再报 500 了
        return DiagnosisResponse(
            disease_name=chinese_pest_name,
            confidence=0.99,
            message="诊断成功" if pest_info else "识别成功，图谱暂无药方",
            treatment=formatted_treatment, 
            expert_report=expert_report
        )

    except Exception as e:
        # 捕捉所有异常，并在终端打印出来方便排查
        print(f"❌ 诊断失败详情: {str(e)}")
        raise HTTPException(status_code=500, detail=f"后端引擎故障: {str(e)}")
        
    finally:
        # 7. 阅后即焚，清理服务器空间
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)