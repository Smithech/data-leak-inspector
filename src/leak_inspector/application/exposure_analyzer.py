from __future__ import annotations

from leak_inspector.domain.enums import ExposureLevel
from leak_inspector.domain.models import FileMetadata, FileExposure


class ExposureResult:
    def __init__(self, level: ExposureLevel):
        self.level = level


class ExposureAnalyzer:
    """
    Analyze file metadata to determine exposure level.

    This analyzer uses file permissions to classify files into:
    - public: accessible by anyone
    - shared: accessible by specific users (domain or muyltiple users)
    - private: only accessible by the owner
    """

    def analyze(self, metadata: FileMetadata) -> ExposureResult:
        """
        Analyze file metadata and return exposure classification.
        """
        #print(type(metadata.permissions[0])
        permissions = metadata.permissions or []
        

        # No permissions → assume PRIVATE
        if not permissions:
            return ExposureResult(ExposureLevel.PRIVATE)

        # PUBLIC → anyone 
        for p in permissions:
            
            if p.get("type") == "anyone":
                return ExposureResult(ExposureLevel.PUBLIC)

        # SHARED → domain or multiple users
        if len(permissions) > 1:
            return ExposureResult(ExposureLevel.SHARED)
        
        for p in permissions:
            if p.get("type") in ("domain", "group"):
                return ExposureResult(ExposureLevel.SHARED)

        # default
        return ExposureResult(ExposureLevel.PRIVATE)