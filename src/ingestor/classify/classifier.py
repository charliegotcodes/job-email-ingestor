
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
    body = message.get("body", "").lower()
    text = f"{subject} {from_msg} {snippet} {body}"


    if any(word in text for word in [ "rejected", "not selected", "unfortunately", "decline", "we regret", "unfortunately", "not moving forward", "will not be moving forward", "we will not be proceeding", "after careful review", "we decided not to move forward"]):
        return "rejected"
    
    if any(phrase in text for phrase in ["update on the status of your application", "still reviewing your application","we are reviewing your application", "whilst we review your application", "thank you for your patience", "due to the high volume of applications"]):
        return "application_update"
    
    if any(word in text for word in [ "your application was sent", "applied on", "application received", "thank you for applying"]):
        return "application"
    
    job_alert_senders = ["invitetoapply", "talent@monster", "alerts@ziprecruiter"]

    if any(sender in from_msg for sender in job_alert_senders):
        return "job_alert"

    if any(word in text for word in ["jobs for you","new jobs","recommended","you may be interested","more new jobs"]):
        return "job_alert"
    
    if any(word in text for word in [ "interview", "call", "phone", "screening", "next step", "available", "availability", "schedule", "meet with"]):
        return "interview"

    if any(phrase in text for phrase in [ "we are pleased to offer you", "offer letter","employment offer"]) and any(word in text for word in ["salary", "compensation","start date"]):
        return "offer"
    
    return "other"

