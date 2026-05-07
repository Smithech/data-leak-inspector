from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.credentials import Credentials as BaseCredentials
from google.oauth2.credentials import Credentials as OAuthCredentials

SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]


def authenticate(credentials_path: Path, token_path: Path) -> BaseCredentials:
    flow = InstalledAppFlow.from_client_secrets_file(
        credentials_path,
        SCOPES,
    )

    creds = flow.run_local_server(port=0)

    token_path.parent.mkdir(parents=True, exist_ok=True)

    with open(token_path, "w") as f:
        f.write(creds.to_json())

    return creds


def load_credentials(token_path: Path) -> BaseCredentials:
    creds = OAuthCredentials.from_authorized_user_file(token_path, SCOPES)

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

        with open(token_path, "w") as f:
            f.write(creds.to_json())

    return creds