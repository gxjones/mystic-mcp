"""
Command line interface for Mystic MCP.
"""

import argparse
import sys

from . import __version__
from .core import MysticMCP


def main():
    """Main entry point for the CLI. This thing will start a MCP server."""
    parser = argparse.ArgumentParser(
        description="Mystic MCP - A Python package for MCP integration"
    )
    parser.add_argument(
        "--version", action="version", version=f"mystic-mcp {__version__}"
    )
    parser.add_argument("--host", help="Host to bind to", default="localhost")
    parser.add_argument("--port", help="Port to bind to", default=8080)

    # subparsers = parser.add_subparsers(dest="command", help="Available commands")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        mcp = MysticMCP()
        mcp.run()

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
