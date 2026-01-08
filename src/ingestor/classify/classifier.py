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

def classify_job_email(message:dict) -> str:
    """Classify if the email message is a job-related email.

    Args:
        message (dict): The email message represented as a dictionary with keys 'subject' and 'from'.

    Returns:
        string variable stating what classification the email belongs to.
        
    """
    subject = message.get("subject", "").lower()
    from_msg = message.get("from", "").lower()
    snippet = message.get("snippet", "").lower()
    body = message.get("body", "")
    text = f"{subject} {from_msg} {snippet}"
    body_text= f"{body}"

    clean_body_text = normalize_whitespace(html_unescape(strip_html_tags(body_text))).lower()

    
    preliminary_category = "other"
    final_category = "other"
    # print(text)


    if any(word in text for word in [ "rejected", "not selected", "unfortunately", "decline", "we regret", "unfortunately", "not moving forward", "will not be moving forward", "we will not be proceeding", "after careful review", "we decided not to move forward"]):
        final_category = "rejected"
    
    elif any(phrase in text for phrase in ["update on the status of your application", "still reviewing your application","we are reviewing your application", "whilst we review your application", "thank you for your patience", "due to the high volume of applications"]):
        preliminary_category = "application_update"
    
    elif any(word in text for word in [ "your application was sent", "applied on", "application received", "thank you for applying", "your application"]):
        preliminary_category = "application"
    
    job_alert_senders = ["invitetoapply", "talent@monster", "alerts@ziprecruiter"]

    if any(sender in from_msg for sender in job_alert_senders):
        final_category = "job_alert"

    elif any(word in text for word in ["jobs for you","new jobs","recommended","you may be interested","more new jobs", "new jobs similar"]):
        final_category = "job_alert"
    
    elif any(word in text for word in [ "interview", "call", "phone", "screening", "next step", "available", "availability", "schedule", "meet with"]):
        final_category = "interview"

    elif any(phrase in text for phrase in [ "we are pleased to offer you", "offer letter","employment offer"]) and any(word in text for word in ["salary", "compensation","start date"]):
        return "offer"

    if preliminary_category in ["application_update", "application"]:
        # print(final_check)
        if strong_rejection_indicators(clean_body_text):
            final_category = "rejected"
        else:
            final_category = preliminary_category
    
    return final_category

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
        "not selected for further consideration"]
    
    for phrase in rejection_phrases:
        if phrase in body:
            return True
    
    return False