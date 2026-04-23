import re

from leak_inspector.domain.models import PIIFinding
from leak_inspector.pii.base import BaseDetector


class EmailDetector(BaseDetector):
    """
    Detector for email addresses.

    This class identifies email addresses within a text using a regular expression.
    If matches are found, it returns a PIIFinding object containing the count and
    sample examples.
    """

    type = "emails"
    pattern = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")

    def detect(self, text: str) -> PIIFinding | None:
        matches = self.pattern.findall(text)

        if not matches:
            return None

        examples = self._extract_examples(matches)

        return PIIFinding(count=len(matches), examples=examples)
