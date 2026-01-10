from email import message
from ingestor.gmail.client import get_gmail_client
from ingestor.gmail.message_reader import read_recent_messages
from ingestor.filters.job_filter import is_job_email
from ingestor.classify.classifier import classify_job_email
from ingestor.clients.jobtracker import send_job_event
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

def main():
    gmail = get_gmail_client()
    messages = read_recent_messages(gmail, max_results=250)
    allowed_categories = ["interview", "offer", "rejected", "application", "application_update"]
    for msg in messages:
        if not is_job_email(msg):
            continue

        category = classify_job_email(msg)
        if category not in allowed_categories:
            continue

        send_job_event(message=msg, category=category, dry_run=False)

if __name__ == "__main__":
    main()
