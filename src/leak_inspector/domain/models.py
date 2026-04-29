from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from .enums import ExposureLevel
from .enums import RiskLevel


class FileMetadata(BaseModel):
    id: str
    name: str
    mime_type: str
    modified_time: datetime
    source: str
    permissions: Optional[List[str]] = None
    web_view_link: Optional[str] = None


class FileContent(BaseModel):
    metadata: FileMetadata
    content: str

    @property
    def id(self) -> str:
        return self.metadata.id


class PIIFinding(BaseModel):
    count: int
    examples: List[str]


class PIISummary(BaseModel):
    emails: Optional[PIIFinding] = None
    phones: Optional[PIIFinding] = None
    credit_cards: Optional[PIIFinding] = None
    names: Optional[PIIFinding] = None

    def total_findings(self) -> int:
        total = 0
        for value in self.model_dump().values():
            if value:
                total += value["count"]
        return total


class ScanResult(BaseModel):
    file_id: str
    modified_time: datetime
    pii_summary: PIISummary | None
    risk_level: RiskLevel | None
    exposure_level: ExposureLevel | None
    source: str


class FileExposure(BaseModel):
    """
    Represents exposure level of a file based on metadata.
    """

    exposure_level: ExposureLevel