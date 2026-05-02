from pathlib import Path
from typing import Any, Dict, List

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]


class GoogleDriveClient:
    def __init__(self, credentials_path: Path, token_path: Path):
        self.credentials_path = credentials_path
        self.token_path = token_path

        self.service = self._authenticate()

    def _authenticate(self):
        creds = None

        if self.token_path.exists():
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)

        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(
                self.credentials_path,
                SCOPES,
            )
            creds = flow.run_local_server(port=0)

            self.token_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.token_path, "w") as token:
                token.write(creds.to_json())

        return build("drive", "v3", credentials=creds)

    def list_files(self) -> List[Dict[str, Any]]:
        """
        List ALL files in Google Drive (excluding folders).
        """

        files = []
        page_token = None

        while True:
            response = (
                self.service.files()
                .list(
                    q="mimeType != 'application/vnd.google-apps.folder'",
                    spaces="drive",
                    fields="nextPageToken, files(id, name, mimeType, modifiedTime, permissions(type, role))",
                    pageToken=page_token,
                )
                .execute()
            )

            files.extend(response.get("files", []))

            page_token = response.get("nextPageToken")

            if not page_token:
                break

        return files
