from sqlalchemy import Column, Integer, String, Date
from app.db.session import Base

class PestRecord(Base):
    __tablename__ = "pest_records" # 在 MySQL 里的真实表名

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    province = Column(String(50), index=True, nullable=False, comment="省份")
    city = Column(String(50), nullable=True, comment="城市")
    pest_name = Column(String(100), nullable=False, comment="病虫害名称")
    report_date = Column(Date, index=True, nullable=False, comment="上报日期")
    severity = Column(Integer, default=1, comment="严重程度 1-5")