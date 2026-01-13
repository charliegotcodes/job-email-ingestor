import re
import html

def strip_html_tags(text: str) -> str:
    """Remove HTML tags from the given text.

    Args:
        text (str): The input text containing HTML tags.

    Returns:
        str: The text with HTML tags removed.
    """

    return re.sub(r"<[^>]+>", "", text)

def html_unescape(text: str) -> str:
    """Unescape HTML entities in the given text.

    Args:
        text (str): The input text containing HTML entities.

    Returns:
        str: The text with HTML entities unescaped.
    """
    
    return html.unescape(text)

def normalize_whitespace(text: str) -> str:
    """Normalize whitespace in the given text.

    Args:
        text (str): The input text containing irregular whitespace.

    Returns:
        str: The text with normalized whitespace.
    """
    return ' '.join(text.split())

def classify_job_email(message: dict) -> str:
    subject = message.get("subject", "").lower()
    from_msg = message.get("from", "").lower()
    snippet = message.get("snippet", "").lower()
    body = message.get("body", "")

    text = f"{subject} {from_msg} {snippet}"
    clean_body_text = normalize_whitespace(html_unescape(strip_html_tags(body))).lower()
    print("BODY LENGTH:", len(clean_body_text))
    # print(clean_body_text)

    # print("TEXT:", text)

    if ("360insights" in subject):
        print(clean_body_text)
    if strong_rejection_indicators(clean_body_text):
        # print(clean_body_text)
        return "rejected"

    job_alert_senders = [
        "invitetoapply@match.indeed.com",
        "talent@monster",
        "alerts@ziprecruiter",
        "mailer@jobleads.com",
        "noreply@jobright.ai",
        "jobs2web.com",
    ]

    if any(sender in text for sender in job_alert_senders):
        return "job_alert"

    if any(word in text for word in [
        "job alert",
        "job matches",
        "new jobs",
        "jobs for you",
        "recommended jobs",
        "apply now",
        "indeed apply",
    ]):
        return "job_alert"

    if any(word in text for word in [
        "interview",
        "screening",
        "availability",
        "schedule",
        "next step",
        "meet with",
    ]):
        return "interview"

    if any(phrase in text for phrase in [
        "we are pleased to offer you",
        "offer letter",
        "employment offer",
    ]) and any(word in text for word in ["salary", "compensation", "start date"]):
        return "offer"

    if any(word in text for word in [
        "application",
        "applied",
        "thank you for applying",
        "application received",
    ]):
        return "application"

    if any(word in text for word in [
        "reviewing your application",
        "application update",
        "status of your application",
    ]):
        return "application_updates"

    return "other"

def strong_rejection_indicators(body: str) -> bool:
    """Check if the email body contains strong rejection indicators.

    Args:
        body (str): The body of the email.

    Returns:
        bool: True if strong rejection indicators are found, False otherwise.
    """
    rejection_phrases = [
        "we regret to inform you",
        "after careful consideration",
        "we have decided not to move forward",
        "we will not be proceeding",
        "not selected for further consideration",
        "move forward",
        "other candidates",
        "after careful review",
        "we decided not to move forward",
        "after careful"
    ]

    for phrase in rejection_phrases:
        if phrase in body:
            return True
    
    return False