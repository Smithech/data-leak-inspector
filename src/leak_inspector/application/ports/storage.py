"""
Storage interface for file sources.

This module defines the contract that any storage implementation
must follow in order to provide files for scanning.

Examples of possible implementations include:

- DemoStorage (local packaged sample files)
- GoogleDriveStorage
- LocalFilesystemStorage
- S3Storage
"""

from abc import ABC, abstractmethod
from typing import Iterable

from leak_inspector.domain.models import FileContent, FileMetadata


class Storage(ABC):
    """
    Abstract interface for file storage providers.

    The scanner interacts with storage exclusively through this interface,
    which allows different backends to be plugged in without modifying
    the scanning logic.
    """

    @abstractmethod
    def list_files(self) -> Iterable[FileMetadata]:
        """
        List available files in the storage system.

        Returns
        -------
        Iterable[FileMetadata]
            Metadata describing each available file.
        """
        pass

    @abstractmethod
    def get_file_content(self, file_metadata: FileMetadata) -> FileContent:
        """
        Retrieve the content of a specific file.

        Parameters
        ----------
        file_id : str
            Unique identifier of the file.

        Returns
        -------
        FileContent
            File metadata and textual content.
        """
        pass
