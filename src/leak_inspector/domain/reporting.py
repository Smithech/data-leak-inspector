"""
Reporting interfaces for exporting scan results.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterable

from leak_inspector.domain.models import ScanResult


class Reporter(ABC):
    """
    Interface for exporting scan results.
    """

    @abstractmethod
    def generate(self, results: Iterable[ScanResult], output: Path) -> None:
        """
        Generate a report from scan results.

        Args:
            results: Iterable of scan results.
            output: Path where the report will be written.
        """
        pass