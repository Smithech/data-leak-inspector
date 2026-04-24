"""
File scanning orchestration service.

This module contains the main application service responsible
for coordinating the file scanning pipeline.

The scanner retrieves files from a storage provider, analyzes
their content for sensitive information, evaluates the risk level,
and produces scan results.
"""

from typing import Iterable

from leak_inspector.application.ports.scan_repository import ScanRepository
from leak_inspector.application.ports.storage import Storage
from leak_inspector.application.risk_evaluator import RiskEvaluator
from leak_inspector.domain.models import ScanResult
from leak_inspector.pii.service import PIIDetectorService
import logging

logger = logging.getLogger(__name__)


class Scanner:
    """
    Coordinates the scanning process across storage,
    PII detection and persistence.
    """

    def __init__(
        self,
        storage: Storage,
        pii_detector: PIIDetectorService,
        risk_evaluator: RiskEvaluator,
        repository: ScanRepository,
    ):
        self.storage = storage
        self.pii_detector = pii_detector
        self.risk_evaluator = risk_evaluator
        self.repository = repository

    def scan(self) -> Iterable[ScanResult]:
        """
        Scan all files from the storage provider.
        """

        logger.info("Starting scan")

        files = list(self.storage.list_files())
        logger.info("Found %d files", len(files))

        for file_metadata in files:
            if self.repository.is_scanned(
                file_metadata.id,
                file_metadata.modified_time,
            ):
                logger.info("Skipping already scanned file: %s", file_metadata.name)
                continue

            file_content = self.storage.get_file_content(file_metadata.id)
            logger.info("Scanning file: %s", file_metadata.name)

            summary = self.pii_detector.analyze(file_content.content)

            risk = self.risk_evaluator.evaluate(summary)

            result = ScanResult(
                file_id=file_metadata.id,
                modified_time=file_metadata.modified_time,
                pii_summary=summary,
                risk_level=risk,
            )

            self.repository.save(result)

            yield result

        logger.info("Scan completed")

        
