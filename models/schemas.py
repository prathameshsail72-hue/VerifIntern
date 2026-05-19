from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship

from config.database import Base


# --- SQLALCHEMY DATABASE MODELS ---
class CompanyModel(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, unique=True, index=True, nullable=False)
    official_domain = Column(String, index=True)
    trust_score = Column(Integer, default=100)
    verification_status = Column(String, default="PENDING")
    created_at = Column(DateTime, default=datetime.utcnow)

    reports = relationship("ScamReportModel", back_populates="company")


class ScamReportModel(Base):
    __tablename__ = "scam_reports"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    communication_channel = Column(String, nullable=False)
    asked_for_money = Column(Boolean, default=False)
    scam_description = Column(Text, nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)

    company = relationship("CompanyModel", back_populates="reports")


# --- PYDANTIC VALIDATION SCHEMAS ---
class ReportSubmit(BaseModel):
    company_name: str
    communication_channel: str
    asked_for_money: bool
    scam_description: str

    class Config:
        from_attributes = True