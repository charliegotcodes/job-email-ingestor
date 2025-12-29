

def is_job_email(message: dict) -> bool:
    """Check if the email message is a job email based on its subject and sender.

    Args:
        message (dict): The email message represented as a dictionary with keys 'subject' and 'from'.

    Returns:
        bool: True if the email is identified as a job email, False otherwise.
    """
    subject = message.get("subject", "").lower()
    from_msg = message.get("from", "").lower()
    snippet = message.get("snippet", "").lower()

    job_keywords = ["applied", "interview", "offer", "thank you for applying", "application"]
    not_job_keywords = ["credit", "bank", "loan", "newsletter"]

    combined_text = f"{subject} {from_msg} {snippet}"
    if any(word in combined_text for word in not_job_keywords):
        return False

    return any(keyword in combined_text for keyword in job_keywords)




