import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.readonly",
]

CREDENTIALS_FILE = os.getenv("GMAIL_CREDENTIALS_FILE", "credentials.json")
TOKEN_FILE = os.getenv("GMAIL_TOKEN_FILE", "token.json")


def get_gmail_service():
    # Build and return Gmail API service with OAuth2 credentials
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(
                    f"Gmail credentials file not found: {CREDENTIALS_FILE}. "
                    "Please download OAuth credentials from Google Cloud Console."
                )
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def create_message(to: str, subject: str, body: str, thread_id: str | None = None) -> dict:
    # Create an email message for the Gmail API
    message = MIMEMultipart()
    message["to"] = to
    message["subject"] = subject
    message.attach(MIMEText(body, "plain"))

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")

    result = {"raw": raw}
    if thread_id:
        result["threadId"] = thread_id

    return result


def send_email(to: str, subject: str, body: str, thread_id: str | None = None) -> dict:
    # Send an email using the Gmail API. This function is used to send emails to a recipient
    service = get_gmail_service()
    message = create_message(to, subject, body, thread_id)

    try:
        sent_message = service.users().messages().send(
            userId="me",
            body=message
        ).execute()
        return sent_message
    except HttpError as error:
        raise Exception(f"Failed to send email: {error}")


def get_thread(thread_id: str) -> dict:
    # Get a Gmail thread by ID

    service = get_gmail_service()
    try:
        thread = service.users().threads().get(userId="me", id=thread_id).execute()
        return thread
    except HttpError as error:
        raise Exception(f"Failed to get thread: {error}")


def check_thread_has_new_messages(thread_id: str, since_message_count: int) -> bool:
    # Check if a thread has received new messages since scheduling.


    try:
        thread = get_thread(thread_id)
        current_count = len(thread.get("messages", []))
        return current_count > since_message_count
    except Exception:
        return False
