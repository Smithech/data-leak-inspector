from datetime import datetime
from pathlib import Path
from typing import Iterable

from leak_inspector.application.ports.storage import Storage
from leak_inspector.domain.models import FileContent, FileMetadata
from leak_inspector.infrastructure.gdrive.client import GoogleDriveClient


class GoogleDriveStorage(Storage):
    """
    Storage implementation for Google Drive.
    """

    def __init__(
            self, 
            client: GoogleDriveClient,
            allowed_extensions: list[str]
    ):
        self.client = client
        self.allowed_extensions = {
            ext.lower() for ext in allowed_extensions
        }

    def list_files(self) -> Iterable[FileMetadata]:
        """
        List files from Google Drive and map them to FileMetadata.
        """

        raw_files = self.client.list_files()

        for file in raw_files:
            extension = Path(file["name"]).suffix.lower()

            if extension in self.allowed_extensions:
                continue

            yield FileMetadata(
                id=file["id"],
                name=file["name"],
                mime_type=file["mimeType"],
                modified_time=datetime.fromisoformat(
                    file["modifiedTime"].replace("Z", "+00:00")
                ),
                source="gdrive",
                permissions=[
                    {
                        "type": p.get("type"),
                        "role": p.get("role"),
                    }
                    for p in file.get("permissions", [])
                ],
                web_view_link=None,
            )

    def get_file_content(self, file_metadata: FileMetadata) -> FileContent:
        """
        Retrieve file content from Google Drive.
        """
        pass

        return FileContent(content=NotImplemented, metadata=NotImplemented)
