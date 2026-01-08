

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


    combined_text = f"{subject} {from_msg} {snippet}"
    # print(combined_text)

    blocked_domains = [ "oesp.ca","ontario.ca"]

    blocked_phrases = ["electricity support", "utility program","credit card", "loan offer","bank statement", "newsletter"]

    if any(domain in from_msg for domain in blocked_domains):
        return False

    if any(phrase in combined_text for phrase in blocked_phrases):
        return False

    job_phrases = ["your application to","your application was sent","thank you for applying","we have received your application","application for the role of","application to"]

    return any(phrase in combined_text for phrase in job_phrases)