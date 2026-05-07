from datetime import datetime
import logging
from typing import Iterable

from leak_inspector.application.ports.storage import Storage
from leak_inspector.config.mime_types import EXTENSION_TO_MIME_TYPES
from leak_inspector.domain.models import FileContent, FileMetadata
from leak_inspector.infrastructure.gdrive.client import GoogleDriveClient


logger = logging.getLogger(__name__)

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
        self.allowed_mime_types: set[str]  = set()

        for ext in allowed_extensions:
            normalized = ext.lower()
            
            #  Allow users to configure: pdf, .pdf
            if not normalized.startswith("."):
                normalized = f".{normalized}"
            
            mime_types = EXTENSION_TO_MIME_TYPES.get(normalized)

            if mime_types is None:
                logger.warning(
                    "Unknown extension configured: %s",
                    normalized,
                )
                continue

            self.allowed_mime_types.update(mime_types)

    def list_files(self) -> Iterable[FileMetadata]:
        """
        List files from Google Drive and map them to FileMetadata.
        """

        raw_files = self.client.list_files()

        for file in raw_files:
            mime_type = file["mimeType"]

            # Empty allowed_mime_types means "allow all files"
            if (
                self.allowed_mime_types
                and mime_type not in self.allowed_mime_types
            ):
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
        raise NotImplementedError(
            "Deep scan mode is not implemented for Google Drive yet."
        )
