"""
CLI rendering utilities using Rich.
"""

from collections import Counter
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from leak_inspector.domain.enums import ScanMode
from leak_inspector.domain.models import ScanResult


console = Console()

def _format_label(label: str, width: int = 7) -> str:
    return label.upper().ljust(width)


def risk_color(risk: str) -> str:
    """
    Map risk levels to terminal colors.
    """

    if risk == "LOW":
        return "green"

    if risk == "MEDIUM":
        return "yellow"

    if risk == "HIGH":
        return "red"

    return "white"


def _render_basic(results):
    print("SCAN RESULTS (BASIC)\n")

    counts = {
        "public": 0,
        "shared": 0,
        "private": 0,
    }

    for result in results:
        level = result.exposure_level.value.upper()
        label = _format_label(level)

        print(f"[{label}] {result.name}")

        counts[result.exposure_level.value] += 1

    print("\nSummary:")
    print(f"  Total files: {len(results)}")
    print(f"  Public: {counts['public']}")
    print(f"  Shared: {counts['shared']}")
    print(f"  Private: {counts['private']}")


def _render_deep(results):
    print("SCAN RESULTS (DEEP)\n")

    counts = {
        "high": 0,
        "medium": 0,
        "low": 0,
    }

    for result in results:
        level = result.risk_level.value
        label = _format_label(level)

        print(f"[{label}] {result.name}")

        if result.pii_summary:
            data = result.pii_summary.model_dump(exclude_none=True)

            if data:
                for key, finding in data.items():
                    print(f"          → {key}: {finding.count} matches")
            else:
                print("          → no sensitive data found")

        counts[level] += 1
        print()

    print("Summary:")
    print(f"  Total files: {len(results)}")
    print(f"  High risk: {counts['high']}")
    print(f"  Medium risk: {counts['medium']}")
    print(f"  Low risk: {counts['low']}")


def render_scan_results(results: list[ScanResult]) -> None:
    """
    Display scan results as a formatted table.
    """
    if not results:
        return
    
    mode = results[0].mode

    if mode == ScanMode.BASIC:
        _render_basic(results)
    else:
        _render_deep(results)