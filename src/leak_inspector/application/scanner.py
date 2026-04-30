"""
File scanning orchestration service.

This module contains the main application service responsible
for coordinating the file scanning pipeline.

The scanner retrieves files from a storage provider, analyzes
their content for sensitive information, evaluates the risk level,
and produces scan results.
"""

import logging
from typing import Iterable

from leak_inspector.application.ports.scan_repository import ScanRepository
from leak_inspector.application.ports.storage import Storage
from leak_inspector.application.exposure_analyzer import ExposureAnalyzer
from leak_inspector.application.risk_evaluator import RiskEvaluator
from leak_inspector.domain.enums import ScanMode
from leak_inspector.domain.models import ScanResult
from leak_inspector.pii.service import PIIDetectorService

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
        mode: ScanMode = ScanMode.BASIC,
        exposure_analyzer: ExposureAnalyzer | None = None,
    ):
        self.storage = storage
        self.pii_detector = pii_detector
        self.risk_evaluator = risk_evaluator
        self.repository = repository
        self.mode = mode
        self.exposure_analyzer = exposure_analyzer or ExposureAnalyzer()

    def scan(self) -> Iterable[ScanResult]:
        """
        Scan all files from the storage provider.
        """

        logger.info("Starting scan")

        logger.debug("Fetching file metadata from storage")

        files = list(self.storage.list_files())
        logger.info("Found %d files", len(files))

        for file_metadata in files:
            logger.debug(
                "Checking if file %s (%s) was already scanned",
                file_metadata.name,
                file_metadata.modified_time,
            )

            if self.repository.is_scanned(
                file_metadata.source,
                file_metadata.id,
                file_metadata.modified_time,
            ):
                logger.info("Skipping already scanned file: %s", file_metadata.name)
                continue

            logger.info("Scanning file: %s", file_metadata.name)

            if self.mode == ScanMode.BASIC:
                exposure = self.exposure_analyzer.analyze(file_metadata)

                result = ScanResult(
                    file_id=file_metadata.id,
                    name=file_metadata.name,
                    source=file_metadata.source,
                    modified_time=file_metadata.modified_time,
                    mode=ScanMode.BASIC,
                    exposure_level=exposure.level,
                    exposure_reason=exposure.reason,
                    pii_summary=None,
                    risk_level=None
                )

            elif self.mode == ScanMode.DEEP:

                logger.debug("Reading file content: %s", file_metadata.name)
                file_content = self.storage.get_file_content(file_metadata)

                logger.debug("Running PII detection")
                summary = self.pii_detector.analyze(file_content.content)

                logger.debug("Evaluating risk level")
                risk = self.risk_evaluator.evaluate(summary)
                
                result = ScanResult(
                    file_id=file_metadata.id,
                    name=file_metadata.name,
                    source=file_metadata.source,
                    modified_time=file_metadata.modified_time,
                    mode=ScanMode.BASIC,
                    exposure_level=None,
                    pii_summary=summary,
                    risk_level=risk
                )
                
            else:
                raise ValueError(f"Unsupported scan mode: {self.mode}")

            logger.debug("Saving scan result to repository")
            self.repository.save(result)

            yield result

        logger.info("Scan completed")
