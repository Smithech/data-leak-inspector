"""
Unit tests for the risk evaluation service.
"""

from leak_inspector.application.risk_evaluator import RiskEvaluator
from leak_inspector.domain.enums import RiskLevel
from leak_inspector.domain.models import PIISummary, PIIFinding


def test_high_risk_credit_card():

    summary = PIISummary(
        credit_cards=PIIFinding(count=1, examples=["4111111111111111"])
    )

    evaluator = RiskEvaluator()
    risk = evaluator.evaluate(summary)
    
    assert risk == RiskLevel.HIGH


def test_medium_risk_many_emails():

    summary = PIISummary(
        emails=PIIFinding(count=5, examples=["a@test.com"])
    )

    evaluator = RiskEvaluator()
    risk = evaluator.evaluate(summary)

    assert risk == RiskLevel.MEDIUM


def test_low_risk_single_email():

    summary = PIISummary(
        emails=PIIFinding(count=1, examples=["a@test.com"])
    )

    evaluator = RiskEvaluator()
    risk = evaluator.evaluate(summary)
    assert risk == RiskLevel.LOW


def test_low_risk_no_pii():

    summary = PIISummary()
    evaluator = RiskEvaluator()
    risk = evaluator.evaluate(summary)
    
    assert risk == RiskLevel.LOW