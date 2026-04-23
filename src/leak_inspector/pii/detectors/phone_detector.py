import re

from leak_inspector.domain.models import PIIFinding
from leak_inspector.pii.base import BaseDetector


class PhoneDetector(BaseDetector):
    """
    Detector for phone numbers.

    This class identifies phone numbers within a text using a regular expression.
    If matches are found, it returns a PIIFinding object containing the count and
    sample examples.
    """

    type = "phones"
    pattern = re.compile(r"\+?\d[\d\s\-]{7,}\d")

    def detect(self, text: str) -> PIIFinding | None:

        matches = self.pattern.findall(text)

        if not matches:
            return None

        examples = self._extract_examples(matches)

        return PIIFinding(
            count=len(matches),
            examples=examples,
        )
