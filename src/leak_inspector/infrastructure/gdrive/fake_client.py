"""
Fake Google Drive client for development and testing.
"""

from datetime import datetime


class FakeGoogleDriveClient:
    """
    Simulates a subset of the Google Drive API.
    """

    def __init__(self):
        self._files = [
            {
                "id": "1",
                "name": "public_notes.txt",
                "modifiedTime": "2024-01-01T10:00:00",
                "mimeType": "text/plain",
                "content": "This is a public document with no sensitive data.",
            },
            {
                "id": "2",
                "name": "employee_contacts.txt",
                "modifiedTime": "2024-01-02T12:00:00",
                "mimeType": "text/plain",
                "content": "Contact john@example.com or call +1 555 123 4567",
            },
            {
                "id": "3",
                "name": "financial_data.txt",
                "modifiedTime": "2024-01-03T15:30:00",
                "mimeType": "text/plain",
                "content": "Credit card: 4111 1111 1111 1111",
            },
        ]

    def list_files(self):
        """
        Simulate listing files from Google Drive.

        Returns:
            List of file metadata dictionaries.
        """
        return [
            {
                "id": f["id"],
                "name": f["name"],
                "modifiedTime": f["modifiedTime"],
                "mimeType": f["mimeType"],
            }
            for f in self._files
        ]

    def download_file(self, file_id: str) -> str:
        """
        Simulate downloading file content.

        Args:
            file_id: ID of the file.

        Returns:
            File content as string.

        Raises:
            ValueError if file not found.
        """
        for f in self._files:
            if f["id"] == file_id:
                return f["content"]

        raise ValueError(f"File with id {file_id} not found")