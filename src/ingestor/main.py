from email import message
from ingestor.gmail.client import get_gmail_client
from ingestor.gmail.message_reader import read_recent_messages
from ingestor.filters.job_filter import is_job_email
from ingestor.classify.classifier import classify_job_email
from ingestor.clients.jobtracker import send_job_event
import logging

from ingestor.gmail.labels import (
    CategoryToLabel,
    get_or_create_label,
    apply_label_to_message,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

def main():
    REMOVE_FROM_INBOX = False
    gmail = get_gmail_client()

    label_cache = {}
    get_or_create_label(gmail, "Jobs", label_cache)
    messages = read_recent_messages(gmail, max_results=200)
    print("MESSAGES FETCHED:", len(messages))
    allowed_categories = list(CategoryToLabel.keys())
    for msg in messages:
        if not is_job_email(msg): 
            print("False")
            continue
        print("True")
        category = classify_job_email(msg)
        print("CATEGORY:", category)
        if category not in allowed_categories:
            continue


        label_name = CategoryToLabel.get(category)
        print("LABEL NAME:", label_name)
        if label_name:
            label_id = get_or_create_label(gmail, label_name, label_cache)
            apply_label_to_message(gmail, msg["id"], label_id, remove_from_inbox=REMOVE_FROM_INBOX)

        send_job_event(message=msg, category=category, dry_run=False)

if __name__ == "__main__":
    main()
