"""
Integration-style unit tests for the scanner.
"""

from datetime import datetime

from leak_inspector.application.ports.scan_repository import ScanRepository
from leak_inspector.application.risk_evaluator import RiskEvaluator
from leak_inspector.application.scanner import Scanner
from leak_inspector.infrastructure.storage.demo_storage import DemoStorage
from leak_inspector.pii.detectors.credit_card_detector import CreditCardDetector
from leak_inspector.pii.detectors.email_detector import EmailDetector
from leak_inspector.pii.detectors.phone_detector import PhoneDetector
from leak_inspector.pii.service import PIIDetectorService


class FakeScanRepository(ScanRepository):
    """
    In-memory repository used for testing.
    """

    def __init__(self):
        self.saved = []
        self.scanned = set()

    def is_scanned(self, source: str, file_id: str, modified_time: datetime) -> bool:
        return (source, file_id, modified_time) in self.scanned

    def save(self, result):
        self.saved.append(result)
        self.scanned.add((result.source, result.file_id, result.modified_time))


def build_scanner():
    """
    Helper function to construct a scanner with demo dependencies.
    """

    storage = DemoStorage()

    pii_service = PIIDetectorService(
        [
            EmailDetector(),
            PhoneDetector(),
            CreditCardDetector(),
        ]
    )

    evaluator = RiskEvaluator()
    repository = FakeScanRepository()
    scanner = Scanner(
        storage=storage,
        pii_detector=pii_service,
        risk_evaluator=evaluator,
        repository=repository,
    )

    return scanner, repository


def test_scanner_returns_results():
    """
    Scanner should return at least one result
    when scanning the demo dataset.
    """

    scanner, _ = build_scanner()

    results = list(scanner.scan())

    assert len(results) > 0


def test_scanner_detects_high_risk_file():
    """
    Scanner should detect at least one HIGH risk file
    in the demo dataset.
    """

    scanner, _ = build_scanner()
    results = scanner.scan()
    high_risk_files = [r for r in results if r.risk_level.value == "HIGH"]

    assert len(high_risk_files) >= 1


def test_scanner_skips_already_scanned_files():
    """
    Scanner should skip files that were already scanned.

    This validates the incremental scanning logic.
    """

    scanner, _ = build_scanner()

    first_run = list(scanner.scan())

    assert len(first_run) > 0

    second_run = list(scanner.scan())

    assert len(second_run) == 0
