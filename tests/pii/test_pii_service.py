"""
Tests for the PII detection service.
"""

from leak_inspector.pii.detectors.email_detector import EmailDetector
from leak_inspector.pii.detectors.phone_detector import PhoneDetector
from leak_inspector.pii.service import PIIDetectorService


def test_service_aggregates_detectors():

    service = PIIDetectorService(
        [
            EmailDetector(),
            PhoneDetector(),
        ]
    )

    text = """
    john@example.com
    +1 555 123 4567
    """

    summary = service.analyze(text)

    assert summary.emails is not None
    assert summary.emails.count == 1
    assert summary.phones is not None
    assert summary.phones.count == 1
