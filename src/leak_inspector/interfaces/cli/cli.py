"""
CLI command definitions for Data Leak Inspector.
"""

import logging
from pathlib import Path
import typer
from typing import NoReturn

from leak_inspector.application.ports.storage import Storage
from leak_inspector.application.risk_evaluator import RiskEvaluator
from leak_inspector.application.scanner import Scanner
from leak_inspector.domain.enums import ScanMode
from leak_inspector.infrastructure.persistence.sqlite_repository import (
    SQLiteScanRepository,
)
from leak_inspector.infrastructure.gdrive.client import GoogleDriveClient
from leak_inspector.infrastructure.reporting.json_reporter import JsonReporter
from leak_inspector.infrastructure.storage.demo_storage import DemoStorage
from leak_inspector.infrastructure.storage.gdrive_storage import GoogleDriveStorage
from leak_inspector.interfaces.cli.render import render_scan_results
from leak_inspector.logging.config import configure_logging
from leak_inspector.pii.registry import load_detectors
from leak_inspector.pii.service import PIIDetectorService

app = typer.Typer(help="Data Leak Inspector CLI")


@app.command()
def auth():
    pass


@app.command()
def scan(
    demo: bool = typer.Option(False, "--demo", help="Use bundled demo files instead of external storage."),
    verbose: bool = typer.Option(False, "--verbose", help="Enable debug logging for detailed output."),
    quiet: bool = typer.Option(False, "--quiet", help="Reduce logging output to warnings and errors only."),
    report: Path | None = typer.Option(
        None, "--report", help="Export scan results to a JSON report file."
    ),
    gdrive: bool = typer.Option(
        False,
        "--gdrive",
        help="Use Google Drive as the storage backend (mock implementation).",
    ),
    mode: ScanMode = typer.Option(
        ScanMode.BASIC,
        "--mode",
        help="Scan mode: basic (metadata) or deep (content analysis).",
    )
):
    """
    Scan files and detect sensitive information (PII).

    Examples:

        dli scan --demo
        dli scan --demo --report report.json
    """

    if verbose:
        level = logging.DEBUG
    elif quiet:
        level = logging.WARNING
    else:
        level = logging.INFO

    configure_logging(level)

    if demo and gdrive:
        _exit_with_error("Cannot use --demo and --gdrive together.")

    if demo:
        typer.echo("Scanning demo dataset...\n")
    elif gdrive:
        typer.echo("Scanning Google Drive...\n")

    storage = _select_storage(demo, gdrive)

    pii_service = PIIDetectorService(load_detectors())

    evaluator = RiskEvaluator()
    repository = SQLiteScanRepository()

    scanner = Scanner(
        storage=storage,
        pii_detector=pii_service,
        risk_evaluator=evaluator,
        repository=repository,
    )

    results = list(scanner.scan())

    if not results:
        typer.echo("No new files to scan.")
        return

    typer.echo()
    
    render_scan_results(results)

    if report:
        reporter = JsonReporter()
        reporter.generate(results, report)
        typer.echo(f"Report written to {report}")


@app.command()
def report():
    pass


def _exit_with_error(message: str) -> NoReturn:
    """
    Print an error message and exit the CLI.
    """
    typer.echo(f"Error: {message}")
    raise typer.Exit(code=1)


def _select_storage(demo: bool, gdrive: bool) -> Storage:
    if demo:
        return DemoStorage()

    if gdrive:
        base = Path("~/Documents/dli").expanduser()

        client = GoogleDriveClient(
            credentials_path=base / "credentials.json",
            token_path=base / "token.json",
        )

        return GoogleDriveStorage(client)

    _exit_with_error("No storage selected. Use --demo or --gdrive.")