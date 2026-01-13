def is_job_email(message: dict) -> bool:
    subject = message.get("subject", "").lower()
    from_msg = message.get("from", "").lower()
    snippet = message.get("snippet", "").lower()

    combined_text = f"{subject} {from_msg} {snippet}"
    # print(combined_text)

    # hard exclusions
    blocked_domains = ["oesp.ca", "ontario.ca", "rhdcc.gc.ca", "creditkarma", "noreply@medium", "hello@passiv", "noreply@marketlog.com", "linkedin@em.linkedin.com", "no-reply@printme.com", "hello@notify.railway.app", "databricks-customer-success@t.databricks.com", "updates-noreply@linkedin.com", "noreply@steampowered.com"]
    blocked_phrases = [
        "electricity support",
        "utility program",
        "credit card",
        "loan offer",
        "bank statement",
        "newsletter",
    ]

    if any(domain in combined_text for domain in blocked_domains):
        return False

    if any(phrase in combined_text for phrase in blocked_phrases):
        return False

    # BROAD job signals (not categories)
    job_signals = [
        "application",
        "applied",
        "candidate",
        "recruit",
        "recruiter",
        "hiring",
        "interview",
        "offer",
        "position",
        "role",
        "career",
        "next step",
        "we regret",
        "unfortunately",
        "jobs"
    ]

    return any(signal in combined_text for signal in job_signals)