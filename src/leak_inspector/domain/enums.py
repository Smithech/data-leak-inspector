from enum import Enum


class RiskLevel(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ScanMode(str, Enum):
    BASIC = "basic"
    DEEP = "deep"


class ExposureLevel(Enum):
    PUBLIC = "public"
    SHARED = "shared"
    PRIVATE = "private"