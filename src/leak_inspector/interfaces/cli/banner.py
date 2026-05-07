import json
import tomllib
import urllib.request

from packaging.version import Version
import typer

PACKAGE_NAME = "data-leak-inspector"

ASCII_LOGO = r"""
   ____  __    ____
  / __ \/ /   /  _/
 / / / / /    / /
/ /_/ / /____/ /
\____/_____/___/
"""


def _load_version() -> str:
    """
    Load the current package version from pyproject.toml.

    Returns:
        str: Current local version defined in the project metadata.
    """
    with open("pyproject.toml", "rb") as f:
        data = tomllib.load(f)

    return data["project"]["version"]


def _get_latest_version() -> str | None:
    """
    Retrieve the latest published version from PyPI.

    Returns:
        str | None:
            Latest available version on PyPI, or None if the
            request fails or the API is unreachable.
    """
    url = f"https://pypi.org/pypi/{PACKAGE_NAME}/json"

    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            data = json.loads(response.read().decode())

        return data["info"]["version"]

    except Exception:
        return None


def _get_update_message() -> str:
    """
    Generate a notification message if a newer version exists on PyPI.

    Returns:
        str:
            Formatted update message when a newer version is available,
            otherwise an empty string.
    """

    current = _load_version()
    latest = _get_latest_version()

    if not latest:
        return ""

    if Version(latest) > Version(current):
        return (
            f"\n🚀 New version available: {latest}\n"
            f"Run: pip install -U {PACKAGE_NAME}\n"
        )

    return ""


def _build_banner() -> str:
    """
    Build the CLI banner including version and update status.

    Returns:
        str:
            Fully formatted banner string ready for terminal output.
    """
    version = _load_version()
    update_message = _get_update_message()

    return f"""
{ASCII_LOGO}
Data Leak Inspector
Version: {version}
        
{update_message}
"""


def render_banner() -> None:
    """
    Render the application banner in the terminal using Typer styling.
    """
    typer.secho(_build_banner(), fg=typer.colors.CYAN)


