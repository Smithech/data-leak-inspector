from datetime import datetime
from typing import Iterable

from leak_inspector.domain.models import FileContent, FileMetadata
from leak_inspector.application.ports.storage import Storage
from leak_inspector.infrastructure.gdrive.client import FakeGoogleDriveClient


class GoogleDriveStorage(Storage):
    """
    Storage implementation for Google Drive.
    """

    def __init__(self, client: FakeGoogleDriveClient):
        self.client = client
    

    def list_files(self) -> Iterable[FileMetadata]:
        """
        List files from Google Drive and map them to FileMetadata.
        """

        raw_files = self.client.list_files()

        for file in raw_files:
            yield FileMetadata(
                id=f"gdrive_{file["id"]}",
                name=file["name"],
                modified_time=datetime.fromisoformat(file["modifiedTime"]),
                mime_type=file["mimeType"],
                permissions=None,
                web_view_link=None
            )
        

    def get_file_content(self, file_metadata: FileMetadata) -> FileContent:
        """
        Retrieve file content from Google Drive.
        """
        if not file_metadata.id.startswith("gdrive_"):
            raise ValueError(f"Invalid gdrive id: {file_metadata.id}")
        
        raw_id = file_metadata.id.replace("gdrive_", "")

        content = self.client.download_file(raw_id)

        return FileContent(
            content=content,
            metadata=file_metadata
        )