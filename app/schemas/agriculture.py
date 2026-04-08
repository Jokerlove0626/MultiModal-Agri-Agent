from pydantic import BaseModel, Field

# 1. 药物信息模型（保持不变，或者根据数据库微调）
class MedicineInfo(BaseModel):
    name: str
    dosage: str | None = None
    description: str | None = None

# 2. 病害详情模型（包含药方列表）
class PestInfo(BaseModel):
    name: str
    common_name: str | None = None
    affected_crops: list[str] = []
    treatments: list[MedicineInfo] = []

# 3. 🚀 最终响应模型：这个最关键！
class DiagnosisResponse(BaseModel):
    disease_name: str = Field(..., description="识别出的中文病害名")
    confidence: float = Field(0.99, description="识别置信度")
    message: str = Field("", description="状态简报")
    
    # 我们把字段名从 pest 改为 treatment，以便对应你 endpoint 里的返回
    treatment: PestInfo | None = Field(None, description="从图谱中找到的详细药方对象")
    
    # 🌟 核心：没有这一行，小作文永远出不来！
    expert_report: str = Field(..., description="Gemini 生成的专家级中文诊断报告")