"""
Logging configuration for Data Leak Inspector.
"""

import logging


def configure_logging(level: int = logging.INFO) -> None:
    """
    Configure application-wide logging.

    Using force=True ensures the configuration is applied even if
    logging has already been initialized by another library.
    """

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
        force=True,
    )
