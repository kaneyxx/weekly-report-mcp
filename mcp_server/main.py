"""
Main entry point for the Weekly Report Checker MCP server.
"""

from mcp_server.weekly_report_server import mcp

def main():
    """Run the MCP server."""
    mcp.run()

if __name__ == "__main__":
    main() 