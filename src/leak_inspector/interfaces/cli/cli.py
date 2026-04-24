"""
CLI command definitions for Data Leak Inspector.
"""

import logging
from pathlib import Path
import typer

from leak_inspector.application.risk_evaluator import RiskEvaluator
from leak_inspector.application.scanner import Scanner
from leak_inspector.infrastructure.persistence.sqlite_repository import (
    SQLiteScanRepository,
)
from leak_inspector.infrastructure.reporting.json_reporter import JsonReporter
from leak_inspector.infrastructure.storage.demo_storage import DemoStorage
from leak_inspector.interfaces.cli.render import render_scan_results, render_summary
from leak_inspector.logging.config import configure_logging
from leak_inspector.pii.detectors.credit_card_detector import CreditCardDetector
from leak_inspector.pii.detectors.email_detector import EmailDetector
from leak_inspector.pii.detectors.phone_detector import PhoneDetector
from leak_inspector.pii.service import PIIDetectorService

app = typer.Typer(help="Data Leak Inspector CLI")


@app.command()
def auth():
    print("Autenticating process...")
    typer.secho("Autenticación exitosa", fg=typer.colors.GREEN)
    typer.secho("Token generado")


@app.command()
def scan(
    demo: bool = typer.Option(False, "--demo", help="Use demo dataset"),
    verbose: bool = typer.Option(False, "--verbose", help="Enable debug logging"),
    quiet: bool = typer.Option(False, "--quiet", help="Reduce logging output"),
    report: Path | None = typer.Option(None, "--report", help="Export scan results to a JSON report file.")
):
    """
    Scan files for sensitive information.
    """

    if verbose:
        level = logging.DEBUG
    elif quiet:
        level = logging.WARNING
    else:
        level = logging.INFO

    configure_logging(level)

    if not demo:
        typer.echo("Currently only demo mode is supported.")
        raise typer.Exit(code=1)

    typer.echo("Scanning demo dataset...\n")

    storage = DemoStorage()

    pii_service = PIIDetectorService(
        [
            EmailDetector(),
            PhoneDetector(),
            CreditCardDetector(),
        ]
    )

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

    render_scan_results(results)

    render_summary(results)

    if report:
        reporter = JsonReporter()
        reporter.generate(results, report)
        typer.echo(f"Report written to {report}")


@app.command()
def report():
    print("📊 Reporte generado")
