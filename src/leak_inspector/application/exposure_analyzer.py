from __future__ import annotations

from leak_inspector.domain.enums import ExposureLevel
from leak_inspector.domain.models import FileMetadata, FileExposure


class ExposureAnalyzer:
    """
    Analyze file metadata to determine exposure level.

    This analyzer uses file permissions to classify files into:
    - public: accessible by anyone
    - shared: accessible by specific users
    - private: only accessible by the owner

    NOTE:
    This is a simplified MVP implementation. Google Drive permissions
    will later provide richer data (roles, domains, etc.).
    """

    def analyze(self, metadata: FileMetadata) -> FileExposure:
        """
        Analyze file metadata and return exposure classification.
        """

        permissions = metadata.permissions

        # No permissions → assume private
        if not permissions:
            return FileExposure(exposure_level=ExposureLevel.PRIVATE)

        permissions = [str(p).lower() for p in permissions]

        permissions = [str(p).lower() for p in permissions]

        if any(p in ("anyone", "public") for p in permissions):
            return FileExposure(exposure_level=ExposureLevel.PUBLIC)

        # Shared file (multiple users or explicit sharing)
        if len(permissions) > 1:
            return FileExposure(exposure_level=ExposureLevel.SHARED)

        # Single permission but not public → shared
        return FileExposure(exposure_level=ExposureLevel.SHARED)