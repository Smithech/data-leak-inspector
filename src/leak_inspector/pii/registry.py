"""
PII detector auto-discovery.
"""

import importlib
import inspect
import pkgutil
from typing import List, Type

from leak_inspector.pii.base import BaseDetector
import leak_inspector.pii.detectors as detectors_pkg
from leak_inspector.pii.detectors.email_detector import EmailDetector
from leak_inspector.pii.detectors.phone_detector import PhoneDetector
from leak_inspector.pii.detectors.credit_card_detector import CreditCardDetector


def _discover_detector_classes() -> List[Type[BaseDetector]]:
    """
    Discover all detector classes in the detectors package.
    """

    detector_classes = []

    for _, module_name, _ in pkgutil.iter_modules(detectors_pkg.__path__):
        module = importlib.import_module(f"{detectors_pkg.__name__}.{module_name}")

        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, BaseDetector) and obj is not BaseDetector:
                detector_classes.append(obj)

    return detector_classes


def load_detectors() -> List[BaseDetector]:
    """
    Instantiate all discovered detectors.
    """
    classes = _discover_detector_classes()

    return sorted([cls() for cls in classes], key=lambda d: d.type)
