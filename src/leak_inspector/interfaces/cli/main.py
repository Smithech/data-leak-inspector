"""
CLI entrypoint.
"""

from leak_inspector.interfaces.cli.cli import app


def main():
    app()


if __name__ == "__main__":
    app()
