"""
File scanning orchestration service.

This module contains the main application service responsible
for coordinating the file scanning pipeline.

The scanner retrieves files from a storage provider, analyzes
their content for sensitive information, evaluates the risk level,
and produces scan results.
"""

from typing import Iterable, List

from leak_inspector.application.ports.storage import Storage
from leak_inspector.application.ports.scan_repository import ScanRepository
from leak_inspector.application.risk_evaluator import RiskEvaluator
from leak_inspector.domain.models import ScanResult
from leak_inspector.pii.service import PIIDetectorService


class Scanner:
    """
    Main application service responsible for scanning files.

    The scanner orchestrates the full analysis pipeline:

    1. Retrieve file metadata from storage
    2. Retrieve file content
    3. Run PII detection
    4. Evaluate risk
    5. Produce scan results

    The scanner is storage-agnostic and depends only on
    abstract interfaces.
    """

    def __init__(
            self,
            storage: Storage,
            pii_service: PIIDetectorService,
            risk_evaluator: RiskEvaluator,
            repository: ScanRepository,
    ):
        """
        Initialize the scanner.

        Parameters
        ----------
        storage : Storage
            File storage provider.

        pii_detector : PIIDetectorService
            Service responsible for detecting PII.

        risk_evaluator : RiskEvaluator
            Service responsible for classifying risk.
        """
        self.storage = storage,
        self.pii_service = pii_service,
        self.risk_evaluator = risk_evaluator
        self.repository = repository

        def scan(self) -> Iterable[ScanResult]:
            """
            Execute a full scan of available files.

            Returns
            -------
            Iterable[ScanResult]
                Scan results for each processed file.
            """

            results: List[ScanResult] = []

            for file_metadata in self.storage.list_files():
                if self.repository.is_scanned(
                    file_metadata.id,
                    file_metadata.modified_time,
                ):
                    continue
                
                file_content = self.storage.get_file_content(file_metadata.id)
                summary = self.pii_detector.analyze(file_content.content)
                risk = self.risk_evaluator.evaluate(summary)

                result = ScanResult(
                    file_id=file_metadata.id,
                    modified_time=file_metadata.modified_time,
                    pii_summary=summary,
                    risk_level=risk
                )
                results.append(result)
            
            return results         