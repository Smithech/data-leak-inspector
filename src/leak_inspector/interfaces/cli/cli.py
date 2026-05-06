"""
CLI command definitions for Data Leak Inspector.
"""

import logging
from pathlib import Path
from typing import NoReturn

import typer
from rich.progress import Progress

from leak_inspector.application.ports.storage import Storage
from leak_inspector.application.risk_evaluator import RiskEvaluator
from leak_inspector.application.scanner import Scanner
from leak_inspector.config.settings import load_settings
from leak_inspector.domain.enums import ScanMode
from leak_inspector.infrastructure.gdrive.auth import load_credentials
from leak_inspector.infrastructure.gdrive.client import GoogleDriveClient
from leak_inspector.infrastructure.persistence.sqlite_repository import (
    SQLiteScanRepository,
)
from leak_inspector.infrastructure.reporting.json_reporter import JsonReporter
from leak_inspector.infrastructure.storage.demo_storage import DemoStorage
from leak_inspector.infrastructure.storage.gdrive_storage import GoogleDriveStorage
from leak_inspector.interfaces.cli.render import render_scan_results
from leak_inspector.logging.config import configure_logging
from leak_inspector.pii.registry import load_detectors
from leak_inspector.pii.service import PIIDetectorService

app = typer.Typer(help="Data Leak Inspector CLI")

settings = load_settings()


@app.command()
def init():
    """
    Initialize DLI configuration and create default config file.
    """
    from leak_inspector.config.settings import AppPaths, default_settings
    import toml

    paths = AppPaths()

    # -------------------------
    # Create directories
    # -------------------------
    paths.config_dir.mkdir(parents=True, exist_ok=True)
    paths.data_dir.mkdir(parents=True, exist_ok=True)

    typer.echo("📁 Directories:")
    typer.echo(f"  Config: {paths.config_dir}")
    typer.echo(f"  Data:   {paths.data_dir}")

    # -------------------------
    # Create config.toml if not exists
    # -------------------------
    if not paths.config_file.exists():
        config_data = default_settings(paths)

        with open(paths.config_file, "w") as f:
            toml.dump(config_data, f)

        typer.secho("\n✅ config.toml created", fg=typer.colors.GREEN)
    else:
        typer.secho("\n⚠ config.toml already exists", fg=typer.colors.YELLOW)

    typer.echo(f"  Path: {paths.config_file}")

    # -------------------------
    # Create reports dir (nice UX)
    # -------------------------
    reports_dir = paths.data_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    # -------------------------
    # Google setup guide
    # -------------------------
    typer.echo("\n🔐 Google Drive setup:")
    typer.echo("1. Go to https://console.cloud.google.com/")
    typer.echo("2. Create a project")
    typer.echo("3. Enable Google Drive API")
    typer.echo("4. Create OAuth Client ID (Desktop App)")
    typer.echo("5. Download credentials.json")

    typer.echo("\n📌 Place credentials.json here:")
    typer.secho(f"  {paths.credentials_path}", fg=typer.colors.CYAN)

    # -------------------------
    # Next steps
    # -------------------------
    typer.echo("\n🚀 Next steps:")
    typer.echo("  dli auth")
    typer.echo("  dli scan --gdrive")


@app.command()
def auth():
    pass


@app.command()
def scan(
    demo: bool = typer.Option(
        False, "--demo", help="Use bundled demo files instead of external storage."
    ),
    verbose: bool = typer.Option(
        False, "--verbose", help="Enable debug logging for detailed output."
    ),
    quiet: bool = typer.Option(
        False, "--quiet", help="Reduce logging output to warnings and errors only."
    ),
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
    ),
):
    """
    Scan files and detect sensitive information (PII).

    Examples:

        dli scan --demo
        dli scan --demo --report report.json
    """
    if demo:
        typer.echo("Scanning demo dataset...\n")
    elif gdrive:
        typer.echo("Scanning Google Drive...\n")

    # -------------------------
    # Logging
    # -------------------------
    if verbose:
        level = logging.DEBUG
    elif quiet:
        level = logging.WARNING
    else:
        level = logging.WARNING

    configure_logging(level)

    # -------------------------
    # Storage selection
    # -------------------------
    if demo and gdrive:
        _exit_with_error("Cannot use --demo and --gdrive together.")

    storage = _select_storage(demo, gdrive)

    # -------------------------
    # Services
    # -------------------------
    pii_service = PIIDetectorService(load_detectors())
    evaluator = RiskEvaluator()
    repository = SQLiteScanRepository()

    scanner = Scanner(
        storage=storage,
        pii_detector=pii_service,
        risk_evaluator=evaluator,
        repository=repository,
    )

    # -------------------------
    # Fetching files
    # -------------------------
    files = []

    with Progress() as progress:
        task = progress.add_task("Fetching files...", total=None)

        for file in storage.list_files():
            files.append(file)
            progress.advance(task)

    if not files:
        typer.secho("No files found.", fg=typer.colors.YELLOW)
        raise typer.Exit()

    typer.echo()

    # -------------------------
    # Scanning files
    # -------------------------

    results = []

    with Progress() as progress:
        task = progress.add_task("Scanning files...", total=len(files))

        for file_metadata in files:
            progress.update(
                task,
                description=f"Scanning {progress.tasks[0].completed + 1}/{len(files)}: ",
            )
            results.extend(scanner.scan_file(file_metadata))
            progress.advance(task)

    # -------------------------
    # Results
    # -------------------------
    if not results:
        typer.secho("No new files to scan.", fg=typer.colors.YELLOW)
        return

    typer.echo()

    render_scan_results(results)

    # -------------------------
    # Reports
    # -------------------------
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
        if not settings.google_token_path.exists():
            _exit_with_error("Not authenticated. Run `dli auth`.")

        creds = load_credentials(settings.google_token_path)
        client = GoogleDriveClient(creds)

        return GoogleDriveStorage(client)

    _exit_with_error("No storage selected. Use --demo or --gdrive.")
