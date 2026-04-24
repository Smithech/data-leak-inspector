"""
CLI rendering utilities using Rich.
"""

from collections import Counter
from rich.console import Console
from rich.panel import Panel
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


def render_summary(results: list[ScanResult]) -> None:
    """
    Display aggregated scan statistics.
    """

    counter = Counter(r.risk_level.value for r in results)

    summary_table = Table.grid(padding=(0, 2))

    summary_table.add_row("Files scanned:", str(len(results)))
    summary_table.add_row("High risk:", f"[red]{counter.get('HIGH', 0)}[/red]")
    summary_table.add_row(
        "Medium risk:", f"[yellow]{counter.get('MEDIUM', 0)}[/yellow]"
    )
    summary_table.add_row("Low risk:", f"[green]{counter.get('LOW', 0)}[/green]")

    console.print()
    console.print(Panel(summary_table, title="Scan Summary"))
