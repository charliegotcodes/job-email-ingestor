
from email.mime import message
import re
import html
import requests
from datetime import datetime
from email.utils import parsedate_to_datetime
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv()
JOBTRACKER_API_URL = os.getenv("JOBTRACKER_API_URL")

def strip_html_tags(text: str) -> str:
    """
    Remove HTML tags from the given text.
    """

    return re.sub(r"<[^>]+>", "", text)

def html_unescape(text: str) -> str:
    """
    Unescape HTML entities in the given text.
    """
    
    return html.unescape(text)

def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace in the given text.
    """
    return ' '.join(text.split())

def extract_company(message: dict) -> str:
    """
    Extract company name from the email message.
    """
    subject = message.get("subject", "")
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

    if " at " in subject and " to " in subject:
        return " ".join(subject.split(" at ")[-1].split()).strip(punctuations)
    elif " at " in subject:
        return " ".join(subject.split(" at ")[-1].split()).strip(punctuations)
    elif " - application" in subject.lower():
            return " ".join(subject.split(" - ")[0].split()).strip(punctuations)
    elif " to " in subject:
        return " ".join(subject.split(" to ")[-1].split()).strip(punctuations)
    elif " from " in subject:
        return " ".join(subject.split(" from ")[-1].split()).strip(punctuations)
    elif " - we" in subject.lower():
        return " ".join(subject.split(" - ")[0].split()).strip(punctuations)
    else:
         return company_check_body(message.get("body", ""))

def company_check_body(message: str) -> str:
     """
     Fallsback extractor when the subject line doesn't include the company.Extract company name from the email message body.
     NEED TO ADD MORE CONDITIONS HERE
     """
     punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
     clean_body_text = normalize_whitespace(html_unescape(strip_html_tags(message))).lower()
     if "thank you for your interest in" in clean_body_text:
        company = clean_body_text.split("thank you for your interest in")[-1].split(".")[0]
        return company.strip(punctuations).strip().title()
     return "Unknown Company"

def extract_position(message: dict, company: str) -> str:
    """
    Extract position title from the email message.
    """
    subject_value = message.get("subject", "").lower()
    body_value = message.get("body", "").lower()
    subject = f"{subject_value}"
    text = f"{body_value}"
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

    clean_body_text = normalize_whitespace(html_unescape(strip_html_tags(text)))
    print("subject: ", subject)
    if " to " in subject and " at " in subject:
        return subject.split(" to ")[-1].split(" at ")[0].title()
    elif " regarding " in subject:
        return subject.split(" regarding ")[-1].split(" at ")[0].title()
    elif " update on your application for " in subject and " at " in subject:
        return subject.split(" update on your application for ")[-1].split(" at ")[0].title().strip(punctuations).strip()
    elif " the role of " in subject and " at " in subject:
        return subject.split(" the role of ")[-1].split(" at ")[0].title().strip(punctuations).strip()
    elif " your application for " in subject.lower() and " - " in subject:
        return subject.split(" your application for ")[-1].split(" - ")[0].title()
    else:
        print("company: ", company)
        return position_check_body(clean_body_text, company=company)

def position_check_body(message: str, company: str) -> str:
     """
     Fallback extractor when the subject line doesn't include the role.
     This handles ATS and LinkedIn confirmation emails where the role
     only appears in the body.
     """
     punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
     clean_body_text = normalize_whitespace(html_unescape(strip_html_tags(message))).lower()
     company_lc = company.lower()

     if "was sent to" in clean_body_text:
        sent_index = clean_body_text.find("was sent to")
        first_index = clean_body_text.find(company_lc, sent_index)
        if first_index != -1:
            second_index = clean_body_text.find(company_lc, first_index + len(company_lc))
            if second_index != -1:
                position = clean_body_text[
                    first_index + len(company_lc):second_index
                ].strip(punctuations).strip()

                if 1 <= len(position.split()) <= 6:
                    return position.title()

     if "application for the" in clean_body_text and " at " in clean_body_text:
        position = clean_body_text.split("application for the")[-1].split(" at ")[0]
        position = position.strip(punctuations).strip()
        if 1 <= len(position.split()) <= 6:
            return position.title()

     if "your application for" in clean_body_text and "[new grads welcome]" in clean_body_text:
        position = clean_body_text.split("your application for")[-1] \
                                  .split("[new grads welcome]")[0]
        position = position.strip(punctuations).strip()
        if 1 <= len(position.split()) <= 6:
            return position.title()

     if "for applying to the" in clean_body_text and "role!" in clean_body_text:
        position = clean_body_text.split("for applying to the")[-1].split("role!")[0]
        position = position.strip(punctuations).strip()
        if 1 <= len(position.split()) <= 6:
            return position.title()

     if "application to the" in clean_body_text and "position" in clean_body_text:
        position = clean_body_text.split("application to the")[-1].split("position")[0]
        position = position.strip(punctuations).strip()
        if 1 <= len(position.split()) <= 6:
            return position.title()

     if "thank you for applying for the" in clean_body_text and "position" in clean_body_text:
        position = clean_body_text.split("thank you for applying for the")[-1] \
                                  .split("position")[0]
        position = position.strip(punctuations).strip()
        if 1 <= len(position.split()) <= 6:
            return position.title()

     if "to our" in clean_body_text and "position" in clean_body_text and "apply" in clean_body_text:
        position = clean_body_text.split("to our")[-1].split("position")[0]
        position = position.strip(punctuations).strip()
        if 1 <= len(position.split()) <= 6:
            return position.title()

     if "to the" in clean_body_text and "position" in clean_body_text:
        position = clean_body_text.split("to the")[-1].split("position")[0]
        position = position.strip(punctuations).strip()
        if 1 <= len(position.split()) <= 5:
            return position.title()

     return "Unknown Position"

def parse_received_at(date_str: str) -> str:
    """
    Parse the received_at date string to the desired format.
    """
    if not date_str:
        return None
    try:
        dt = parsedate_to_datetime(date_str)
        return dt.astimezone().isoformat()
    except Exception:
        return None


def send_job_event(message: dict, category: str, dry_run: bool = True) -> dict:
    """
    Build and send a job event to the JobTracker API.
    Returns the payload that was sent.
    """
    company = extract_company(message)
    position = extract_position(message, company=company)
    received_at = parse_received_at(message.get("date"))

    payload ={
        'source': 'gmail',
        'external_id': message['id'],
        'category': category,
        'company': company,
        'position': position,
        'received_at': received_at,
        'raw_subject': message.get('subject', ''),
    }
    logger.info("Sending job event", extra={"payload": payload})
    
    if dry_run:
        return payload

    response = requests.post(
        f"{JOBTRACKER_API_URL}/events",
        json=payload,
        timeout=5,
    )

    if response.status_code not in (200, 201, 409):
        raise RuntimeError(
            f"JobTracker API error {response.status_code}: {response.text}"
        )

    return payload