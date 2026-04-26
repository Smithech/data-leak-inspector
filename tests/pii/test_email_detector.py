"""
Unit tests for the email PII detector.
"""

from leak_inspector.pii.detectors.email_detector import EmailDetector


def test_detect_single_email():

    detector = EmailDetector()
    text = "Contact me at john@example.com"
    result = detector.detect(text)

    assert result is not None
    assert result.count == 1
    assert "john@example.com" in result.examples


def test_detect_multiple_emails():

    detector = EmailDetector()

    text = """
    john@example.com
    jane@test.org
    admin@company.net
    """

    result = detector.detect(text)

    assert result is not None
    assert result.count == 3


def test_no_email_returns_none():

    detector = EmailDetector()
    text = "There is no sensitive data here."
    result = detector.detect(text)

    assert result is None
