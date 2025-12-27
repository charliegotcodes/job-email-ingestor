from typing import List, Dict, Optional


def _get_header(headers, name):
    for header in headers:
        if header.get("name", "").lower() == name.lower():
            return header.get("value")
    return None 

def _parse_message(gmail, message_id):
    message = gmail.users().messages().get(userId="me", id = message_id).execute()
    snippet = message.get("snippet", "")
    payload = message.get("payload", {})
    headers = payload.get("headers", [])
    return{
        "id": message_id,
        "from": _get_header(headers, "from"),
        "subject": _get_header(headers, "subject"),
        "date": _get_header(headers, "date"),
        "snippet": snippet
    }

def read_recent_messages(gmail, max_results):
    response = gmail.users().messages().list(userId="me", maxResults=max_results).execute()
    messages = response.get("messages", [])
    parsed_messages = []
    for msg in messages:
        message_id = msg.get("id")
        if not message_id:
            continue
        parsed_messages.append(_parse_message(gmail, message_id))

    return parsed_messages