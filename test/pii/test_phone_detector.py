"""
Unit tests for the phone number PII detector.
"""

from leak_inspector.pii.detectors.phone_detector import PhoneDetector


def test_detect_phone_number():

    detector = PhoneDetector()
    text = "Call me at +1 555 123 4567"
    result = detector.detect(text)

    assert result is not None
    assert result.count == 1
    assert "+1 555 123 4567" in result.examples


def test_no_phone_returns_none():

    detector = PhoneDetector()
    text = "This file contains only notes."
    result = detector.detect(text)

    assert result is None
