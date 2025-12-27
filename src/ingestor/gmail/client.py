
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPE = ['https://www.googleapis.com/auth/gmail.modify']
BASE_DIR = Path(__file__).resolve().parents[3]
CREDENTIALS_PATH = BASE_DIR / "credentials" / "credential.json"
TOKEN_PATH = BASE_DIR / "credentials" / "token.json"

def get_gmail_client():
    if not CREDENTIALS_PATH.exists():
        raise FileNotFoundError(f"Credentials file not found at {CREDENTIALS_PATH}")

    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPE)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_PATH), SCOPE)
            creds = flow.run_local_server(port=0)

        TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
        TOKEN_PATH.write_text(creds.to_json())

    service = build("gmail", "v1", credentials=creds)
    return service
