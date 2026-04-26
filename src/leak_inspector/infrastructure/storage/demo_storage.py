"""
Demo storage implementation.

This storage backend provides access to a set of packaged
sample files that are included with the project. It is used
to demonstrate the capabilities of the scanner without
requiring any external storage integration.
"""

from datetime import datetime
from importlib import resources
from typing import Iterable

from leak_inspector.application.ports.storage import Storage
from leak_inspector.domain.models import FileContent, FileMetadata


class DemoStorage(Storage):
    """
    Storage implementation that reads bundled sample files.

    The files are packaged inside the project and accessed using
    importlib.resources so that they work both in development
    environments and when the package is installed from PyPI.
    """

    PACKAGE = "leak_inspector.data.sample_files"

    def list_files(self) -> Iterable[FileMetadata]:
        """
        List all demo files bundled with the package.
        """

        files = []

        for resource in resources.files(self.PACKAGE).iterdir():
            if resource.name.endswith(".txt"):
                files.append(
                    FileMetadata(
                        id=resource.name,
                        name=resource.name,
                        mime_type="text/plain",
                        modified_time=datetime(2024, 1, 1),
                        source="demo",
                        permissions=None,
                        web_view_link=None,
                    )
                )

        return files

    def get_file_content(self, file_metadata: FileMetadata) -> FileContent:
        """
        Retrieve the content of a specific demo file.
        """

        resource = resources.files(self.PACKAGE).joinpath(file_metadata.id)
        text = resource.read_text()

        return FileContent(
            metadata=file_metadata,
            content=text,
        )
