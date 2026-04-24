"""
CLI rendering utilities using Rich.
"""

from rich.console import Console
from rich.table import Table

from leak_inspector.domain.models import ScanResult


console = Console()


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


def render_scan_results(results: list[ScanResult]) -> None:
    """
    Display scan results as a formatted table.
    """

    table = Table(title="Scan Results")

    table.add_column("File", style="cyan", no_wrap=True)
    table.add_column("Risk", justify="center")

    for result in results:
        color = risk_color(result.risk_level.value)

        table.add_row(
            result.file_id,
            f"[{color}]{result.risk_level.value}[/{color}]",
        )

    console.print(table)