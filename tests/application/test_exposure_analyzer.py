from datetime import datetime

from leak_inspector.application.exposure_analyzer import ExposureAnalyzer
from leak_inspector.domain.enums import ExposureLevel
from leak_inspector.domain.models import FileMetadata


def make_metadata(permissions=None):
    return FileMetadata(
        id="1",
        name="test.txt",
        mime_type="text/plain",
        modified_time=datetime.now(),
        source="test",
        permissions=permissions,
        web_view_link=None,
    )


def test_private_file():
    metadata = make_metadata(permissions=None)

    result = ExposureAnalyzer().analyze(metadata)

    assert result.exposure_level == ExposureLevel.PRIVATE


def test_public_file():
    metadata = make_metadata(permissions=["public"])

    result = ExposureAnalyzer().analyze(metadata)

    assert result.exposure_level == ExposureLevel.PUBLIC


def test_shared_file_multiple_users():
    metadata = make_metadata(permissions=["user:a", "user:b"])

    result = ExposureAnalyzer().analyze(metadata)

    assert result.exposure_level == ExposureLevel.SHARED


def test_shared_file_single_user():
    metadata = make_metadata(permissions=["user:a"])

    result = ExposureAnalyzer().analyze(metadata)

    assert result.exposure_level == ExposureLevel.SHARED