from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from models.schemas import CompanyModel, ScamReportModel
from services.scoring import calculate_trust_score
from services.scraper import get_domain_age_months

router = APIRouter(prefix="/api", tags=["Search Engine"])


@router.get("/search")
def search_company(name: str, db: Session = Depends(get_db)):
    clean_name = name.strip().lower()

    # Query DB for matching name
    company = db.query(CompanyModel).filter(CompanyModel.company_name.ilike(clean_name)).first()

    # If it's a completely new query, pre-seed it into the directory
    if not company:
        domain_guess = f"{clean_name.replace(' ', '')}.com"
        company = CompanyModel(company_name=name.strip(), official_domain=domain_guess)
        db.add(company)
        db.commit()
        db.refresh(company)

    # Fetch total and extreme scam metrics
    reports = db.query(ScamReportModel).filter(ScamReportModel.company_id == company.id).all()
    total_reports = len(reports)
    money_demanded_count = sum(1 for r in reports if r.asked_for_money)

    # Calculate live score metric updates
    months_old = get_domain_age_months(company.official_domain)
    final_score, status = calculate_trust_score(months_old, total_reports, money_demanded_count)

    # Cache calculations back to db profile
    company.trust_score = final_score
    company.verification_status = status
    db.commit()

    return {
        "company_name": company.company_name,
        "domain": company.official_domain,
        "domain_age_months": months_old,
        "total_scam_reports": total_reports,
        "money_demanded_reports": money_demanded_count,
        "trust_score": final_score,
        "verification_status": status,
    }