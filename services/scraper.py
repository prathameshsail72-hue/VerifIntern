from datetime import datetime
import whois


def get_domain_age_months(domain: str) -> int:
    try:
        domain_info = whois.whois(domain)
        creation_date = domain_info.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if not creation_date:
            return 0

        age_days = (datetime.now() - creation_date).days
        return max(0, int(age_days / 30))
    except Exception:
        # Fallback to zero (flagging as high-risk new domain) if WHOIS fails
        return 0