"""
Repository interface for scan results persistence.

This module defines the contract for storing and retrieving
file scan results.
"""

from abc import ABC, abstractmethod
from datetime import datetime

from leak_inspector.domain.models import FileMetadata, ScanResult


class ScanRepository(ABC):
    """
    Abstract repository for persisting scan results.
    """

    @abstractmethod
    def is_scanned(self, file_metadata: FileMetadata) -> bool:
        """
        Check whether a specific file version has already been scanned.
        """
        pass

    @abstractmethod
    def save(self, result: ScanResult) -> None:
        """
        Persist a scan result.
        """
        pass
