from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from models.schemas import CompanyModel, ReportSubmit, ScamReportModel

router = APIRouter(prefix="/api", tags=["Reporting Engine"])


@router.post("/report")
def report_scam(data: ReportSubmit, db: Session = Depends(get_db)):
    clean_name = data.company_name.strip().lower()

    # Locate parent entity or instantiate silently
    company = db.query(CompanyModel).filter(CompanyModel.company_name.ilike(clean_name)).first()
    if not company:
        domain_guess = f"{clean_name.replace(' ', '')}.com"
        company = CompanyModel(company_name=data.company_name.strip(), official_domain=domain_guess)
        db.add(company)
        db.commit()
        db.refresh(company)

    # Create and link new scam log entry
    new_report = ScamReportModel(
        company_id=company.id,
        communication_channel=data.communication_channel,
        asked_for_money=data.asked_for_money,
        scam_description=data.scam_description,
    )
    db.add(new_report)
    db.commit()

    return {"status": "success", "message": "Your report was processed securely."}