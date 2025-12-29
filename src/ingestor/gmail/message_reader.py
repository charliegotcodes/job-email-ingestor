from typing import List, Dict, Optional
import base64


def _get_header(headers, name):
    for header in headers:
        if header.get("name", "").lower() == name.lower():
            return header.get("value")
    return None 

def _parse_message(gmail, message_id):
    message = gmail.users().messages().get(userId="me", id = message_id, format="full").execute()
    payload = message.get("payload", {})
    headers = payload.get("headers", [])

    subject = _get_header(headers, "Subject")
    from_msg = _get_header(headers, "From")
    date = _get_header(headers, "Date")
    snippet = message.get("snippet", "")
    body = _get_body_text(payload)
    return{
        "id": message_id,
        "from": _get_header(headers, "from"),
        "subject": _get_header(headers, "subject"),
        "date": _get_header(headers, "date"),
        "snippet": snippet,
        "body": body
    }

def _get_body_text(payload: dict) -> str:
    if "parts" in payload:
        for part in payload['parts']:
            if part.get('mimeType') == 'text/plain':
                data = part['body'].get('data', '')
                if data:
                    return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
    else:
        data = payload.get('body', {}).get('data', '')
        if data:
            return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
    return ""

def read_recent_messages(gmail, max_results):
    response = gmail.users().messages().list(userId="me", q="category:primary", maxResults=max_results).execute()
    messages = response.get("messages", [])
    parsed_messages = []
    for msg in messages:
        message_id = msg.get("id")
        if not message_id:
            continue
        parsed_messages.append(_parse_message(gmail, message_id))

    return parsed_messages