import re
from abc import ABC, abstractmethod
from typing import List

from leak_inspector.domain.models import PIIFinding


class BaseDetector(ABC):
    """
    Base class for all PII detectors.
    """

    type: str
    pattern: re.Pattern

    MAX_EXAMPLES = 3

    @abstractmethod
    def detect(self, text: str) -> PIIFinding | None:
        pass

    def _extract_examples(self, matches: List[str]) -> List[str]:
        unique = list(dict.fromkeys(matches))
        return unique[: self.MAX_EXAMPLES]
