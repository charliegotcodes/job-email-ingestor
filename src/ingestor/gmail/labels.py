from typing import Dict

CategoryToLabel: Dict[str, str] = {
    "application": "Jobs/Applied",
    "application_updates": "Jobs/Updates",
    "interview": "Jobs/Interview",
    "offer": "Jobs/Offer",
    "rejected": "Jobs/Rejected",
}
LABEL_COLORS = {
    "Jobs/Applied": {
        "backgroundColor": "#FBBC04",
        "textColor": "#000000",
    },
    "Jobs/Interview": {
        "backgroundColor": "#F28B82", 
        "textColor": "#000000",
    },
    "Jobs/Offer": {
        "backgroundColor": "#34A853", 
        "textColor": "#FFFFFF",
    },
    "Jobs/Rejected": {
        "backgroundColor": "#EA4335",  
        "textColor": "#FFFFFF",
    },
    "Jobs/Updates": {
        "backgroundColor": "#4285F4", 
        "textColor": "#FFFFFF",
    },
}

def get_or_create_label(gmail, label_name: str, cache: Dict[str, str]) -> str:
    """
    Get or create Gmail label for the given job email category.
    """
    if label_name in cache:
        return cache[label_name]
    
    resp = gmail.users().labels().list(userId="me").execute()
    labels = resp.get("labels", [])

    for label in labels: 
        if label['name'] == label_name:
            cache[label_name] = label['id']
            return label['id']
    
    body = {
        'name': label_name,
        'labelListVisibility': 'labelShow',
        'messageListVisibility': 'show',
    }

    created = gmail.users().labels().create(userId="me", body=body).execute()
    label_id = created['id']
    

    if label_name in LABEL_COLORS:
        try:
            gmail.users().labels().update(
                userId="me",
                id=label_id,
                body={"color": LABEL_COLORS[label_name]},
            ).execute()
        # Added as a safeguard since not all Gmail accounts support label colors (will add proper label color support later)
        except Exception as e:
            print(f"Failed to set color for {label_name}: {e}")
    
    cache[label_name] = created['id']

    return created['id']

def apply_label_to_message(gmail, message_id: str, label_id: str, remove_from_inbox: bool = True) -> None:
    """
    Apply label to message.
    """
    body = {
        "addLabelIds": [label_id]
    }

    if remove_from_inbox:
        body["removeLabelIds"] = ["INBOX"]

    gmail.users().messages().modify(
        userId="me",
        id=message_id,
        body=body,
    ).execute()
