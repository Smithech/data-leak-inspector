"""
Risk evaluation logic for scanned files.

This module contains the service responsible for converting
a PII detection summary into a risk classification.
"""

from leak_inspector.domain.enums import RiskLevel
from leak_inspector.domain.models import PIISummary


class RiskEvaluator:
    """
    Determines the risk level of a file based on detected PII.

    The evaluator applies a set of simple rules to determine whether
    the presence and volume of detected sensitive information should
    be classified as LOW, MEDIUM, or HIGH risk.

    The rules implemented here are intentionally simple for the MVP
    and can be extended in future versions.
    """

    EMAIL_MEDIUM_THRESHOLD = 5
    NAME_MEDIUM_THRESHOLD = 10

    def evaluate(self, summary: PIISummary) -> RiskLevel:
        """
        Evaluate the risk level for a given PII summary.

        Parameters
        ----------
        summary : PIISummary
            Aggregated PII detection results.

        Returns
        -------
        RiskLevel
            The evaluated risk classification.
        """

        if self._has_credit_cards(summary):
            return RiskLevel.HIGH

        if self._has_medium_risk(summary):
            return RiskLevel.MEDIUM

        if summary.total_findings() > 0:
            return RiskLevel.LOW

        return RiskLevel.LOW

    def _has_credit_cards(self, summary: PIISummary) -> bool:
        """
        Check whether any credit card numbers were detected.
        """

        return bool(summary.credit_cards and summary.credit_cards.count > 0)

    def _has_medium_risk(self, summary: PIISummary) -> bool:
        """
        Determine whether the detected PII meets medium-risk thresholds.
        """

        if summary.phones and summary.phones.count > 0:
            return True

        if summary.emails and summary.emails.count >= self.EMAIL_MEDIUM_THRESHOLD:
            return True

        if summary.names and summary.names.count >= self.NAME_MEDIUM_THRESHOLD:
            return True

        return False
