from ingestor.gmail.client import get_gmail_client
from ingestor.gmail.message_reader import read_recent_messages
from ingestor.filters.job_filter import is_job_email
from ingestor.classify.classifier import classify_job_email


def main():
    gmail = get_gmail_client()
    messages = read_recent_messages(gmail, max_results=30)
    for msg in messages:
        if is_job_email(msg):
            category = classify_job_email(msg)
            print(f"Category: {category.upper()}, msg: {msg['subject']}")
        else:
            print("Not a job email")
    

if __name__ == "__main__":
    main()
