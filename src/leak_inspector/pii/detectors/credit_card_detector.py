import re

from leak_inspector.domain.models import PIIFinding
from leak_inspector.pii.base import BaseDetector


class CreditCardDetector(BaseDetector):
    """
    Detector for credit card numbers.

    This class identifies credit card numbers within a text using a regular expression.
    If matches are found, it returns a PIIFinding object containing the count and
    sample examples.
    """

    type = "credit_cards"

    pattern = re.compile(r"\b(?:\d[ -]*?){13,16}\b")

    def detect(self, text: str):

        matches = self.pattern.findall(text)

        if not matches:
            return None

        examples = self._extract_examples(matches)

        return PIIFinding(
            count=len(matches),
            examples=examples,
        )
