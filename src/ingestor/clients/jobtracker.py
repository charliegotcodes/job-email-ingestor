
from email.mime import message
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

def extract_company(message: dict) -> str:
    """Extract company name from the email message.

    Args:
        message (dict): The email message represented as a dictionary with keys 'subject' and 'from'.

    Returns:
        string variable stating the company name.
        
    """
    subject = message.get("subject", "")
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    # from_msg = message["from"].lower()

    if " at " in subject and " to " in subject:
        return "".join(subject.split(" at ")[-1].strip(punctuations))
    elif " - application" in subject:
            return " ".join(subject.split(" - ")[0]).strip(punctuations)
    elif " to " in subject:
        return " ".join(subject.split(" to ")[-1].split()).strip(punctuations)
    elif " from " in subject:
        return " ".join(subject.split(" from ")[-1].split()).strip(punctuations)
    else:
         pass
    # elif "<" in from_msg and ">" in from_msg:
    #     return from_msg.split("<")[0].strip().title()
    
    # Intend to implement using body text to check for company name

    # Current Fallback
    return "Unknown Company"

def extract_position(message: dict) -> str:
    """Extract position title from the email message.

    Args:
        message (dict): The email message represented as a dictionary with keys 'subject' and 'from'.

    Returns:
        string variable stating the position title.
        
    """
    subject_value = message.get("subject", "").lower()
    body_value = message.get("body", "").lower()
    subject = f"{subject_value}"
    text = f"{body_value}"

    clean_body_text = normalize_whitespace(html_unescape(strip_html_tags(text))).lower()
    
    if " to " in subject and " at " in subject:
        return subject.split(" to ")[-1].split(" at ")[0].title()
    elif " regarding " in subject:
        return subject.split(" regarding ")[-1].split(" at ")[0].title()
    # elif " about " in subject:
    #     return subject.split(" about ")[-1].split(" at ")[0].title()
    else:
        return position_check_body(clean_body_text)
        
    # return "Unknown Position"

def position_check_body(message: str) -> str:
     """
     Extract position title from the email message body.
     """
     body_value = message
     if "to our " in body_value and " position" in body_value:
         return body_value.split("to our")[-1].split("position")[0].title()
     elif "to the " in body_value and " position" in body_value:
         return body_value.split("to the")[-1].split("position")[0].title()
     return "Unknown Position"

def send_job_event(message: dict, category: str) -> dict:
    """
    Build and send a job event to the JobTracker API.
    Returns the payload that was sent.
    """
    company = extract_company(message)
    position = extract_position(message)
    recieved_at = message.get('date')

    payload ={
        'source': 'gmail',
        'external_id': message['id'],
        'category': category,
        'company': company,
        'position': position,
        'recieved_at': recieved_at,
        'raw_subject': message.get('subject', ''),
    }
    print(payload)
    return payload