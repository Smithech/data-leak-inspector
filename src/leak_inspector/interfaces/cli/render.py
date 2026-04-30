"""
CLI rendering utilities using Rich.
"""

from collections import Counter
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import typer

from leak_inspector.domain.enums import ScanMode
from leak_inspector.domain.models import ScanResult

console = Console()

RISK_PRIORITY = {
    "high": 0,
    "medium": 1,
    "low": 2,
}

EXPOSURE_PRIORITY = {
    "public": 0,
    "shared": 1,
    "private": 2,
}

def _format_label(label: str, width: int = 7) -> str:
    return label.upper().ljust(width)


def _color_for_exposure(level: str):
    return {
        "public": typer.colors.RED,
        "shared": typer.colors.YELLOW,
        "private": typer.colors.GREEN,
    }[level]


def _color_for_risk(level: str):
    return {
        "high": typer.colors.RED,
        "medium": typer.colors.YELLOW,
        "low": typer.colors.GREEN,
    }[level]


def _render_basic(results):
    print("SCAN RESULTS (BASIC)\n")

    results = sorted(
        results,
        key=lambda r: (
            EXPOSURE_PRIORITY.get(r.exposure_level.value if r.exposure_level else "private", 99),
            r.name or "",
        )
    )

    counts = {
        "public": 0,
        "shared": 0,
        "private": 0,
    }

    counts = {"public": 0, "shared": 0, "private": 0}

    for result in results:
        level = result.exposure_level.value
        label = _format_label(level)
        color = _color_for_exposure(level)

        typer.secho(f"[{label}]", fg=color, bold=True, nl=False)
        typer.echo(f" {result.name}")

        counts[level] += 1

    typer.echo("\nSummary:")
    typer.echo(f"  Total files: {len(results)}")
    typer.echo(f"  Public: {counts['public']}")
    typer.echo(f"  Shared: {counts['shared']}")
    typer.echo(f"  Private: {counts['private']}")


def _render_deep(results):
    print("SCAN RESULTS (DEEP)\n")

    results = sorted(
        results,
        key=lambda r: (
            RISK_PRIORITY.get(r.risk_level.value if r.risk_level else "low", 99),
            r.name or "",
        )
    )

    counts = {
        "high": 0,
        "medium": 0,
        "low": 0,
    }

    for result in results:
        level = result.risk_level.value
        label = _format_label(level)
        color = _color_for_exposure(level)

        typer.secho(f"[{label}]", fg=color, bold=True, nl=False)
        typer.echo(f" {result.name}")

        if result.pii_summary:
            data = result.pii_summary.model_dump(exclude_none=True)

            if data:
                for key, finding in data.items():
                    typer.echo(f"          → {key}: {finding.count} matches")
            else:
                typer.echo("          → no sensitive data found")

        counts[level] += 1
        typer.echo()

    typer.echo("Summary:")
    typer.echo(f"  Total files: {len(results)}")
    typer.echo(f"  High risk: {counts['high']}")
    typer.echo(f"  Medium risk: {counts['medium']}")
    typer.echo(f"  Low risk: {counts['low']}")


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