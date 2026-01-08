from ingestor.gmail.client import get_gmail_client
from ingestor.gmail.message_reader import read_recent_messages
from ingestor.filters.job_filter import is_job_email
from ingestor.classify.classifier import classify_job_email
from ingestor.clients.jobtracker import send_job_event


def main():
    gmail = get_gmail_client()
    messages = read_recent_messages(gmail, max_results=250)
    allowed_categories = ["interview", "offer", "rejected", "application", "application_update"]
    for msg in messages:
        if is_job_email(msg):
            # print(f"passes: {msg['subject']}")
            category = classify_job_email(msg)
            if category in allowed_categories:
                print(f"Category: {category.upper()}, msg: {msg['subject']}")
                # print("Sending job event")
                send_job_event(msg, category)
        # else:
        #     print("Not a job email")
    

if __name__ == "__main__":
    main()
