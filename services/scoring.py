def calculate_trust_score(domain_age_months: int, total_reports: int, money_demanded_count: int) -> tuple[int, str]:
    # Base Score starts perfect
    score = 100

    # 1. Domain Age Penalty (Under 6 months is a major red flag)
    if domain_age_months < 6:
        score -= 15

    # 2. Crowd-sourced Flag Penalties
    # Standard reports cost 10 points; reports demanding money cost an additional 15 points (total 25)
    report_penalty = (total_reports * 10) + (money_demanded_count * 15)
    score -= report_penalty

    # Keep boundaries between 0 and 100
    final_score = max(0, min(score, 100))

    # 3. Dynamic Category Assignment
    if final_score >= 75:
        status = "VERIFIED / SAFE"
    elif final_score >= 45:
        status = "SUSPICIOUS / CAUTION"
    else:
        status = "FLAGGED SCAM"

    return final_score, status