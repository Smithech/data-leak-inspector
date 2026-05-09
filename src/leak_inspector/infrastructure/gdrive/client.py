from pathlib import Path
from typing import Any, Dict, List

from google.auth.credentials import Credentials
from googleapiclient.discovery import build


class GoogleDriveClient:
    def __init__(self, credentials: Credentials):
        self.service = build("drive", "v3", credentials=credentials)

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
                    q=(
                        "mimeType != 'application/vnd.google-apps.folder'"
                        "and 'me' in owners "
                        "and trashed = false"
                    ),
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
