from typing import List

from leak_inspector.domain.models import PIISummary
from leak_inspector.pii.base import BaseDetector


class PIIDetectorService:
    """
    Service to manage PII detection.

    This class aggregates multiple PII detectors and provides a method to analyze text for
    potential PII leaks. It returns a summary of findings across all detectors.
    """

    def __init__(self, detectors: List[BaseDetector]):
        self.detectors = detectors

    def analyze(self, text: str) -> PIISummary:
        summary = PIISummary()

        for detector in self.detectors:
            finding = detector.detect(text)

            if finding:
                setattr(summary, detector.type, finding)

        return summary
