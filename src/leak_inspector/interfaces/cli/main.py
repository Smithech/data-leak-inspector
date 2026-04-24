"""
CLI entrypoint.
"""

from leak_inspector.interfaces.cli.cli import app
from leak_inspector.logging.config import configure_logging


def main():
    configure_logging()
    app()


if __name__ == "__main__":
    main()
