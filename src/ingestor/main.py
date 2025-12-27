from ingestor.gmail.client import get_gmail_client
from ingestor.gmail.message_reader import read_recent_messages


def main():
    gmail = get_gmail_client()
    messages = read_recent_messages(gmail, max_results=10)

    for msg in messages:
        print(msg)

if __name__ == "__main__":
    main()
