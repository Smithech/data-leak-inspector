"""
Unit tests for the credit card detector.
"""

from leak_inspector.pii.detectors.credit_card_detector import CreditCardDetector


def test_detect_credit_card():

    detector = CreditCardDetector()
    text = "Card number: 4111 1111 1111 1111"
    result = detector.detect(text)

    assert result is not None
    assert result.count == 1
    assert "4111 1111 1111 1111" in result.examples


def test_no_credit_card_returns_none():

    detector = CreditCardDetector()
    text = "This document contains no financial data."
    result = detector.detect(text)

    assert result is None
