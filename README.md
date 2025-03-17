```markdown
# Weekly Report Checker MCP Server

An MCP (Model Context Protocol) server that checks weekly report submissions in a Google Sheet.

## Features

- Check who hasn't submitted their weekly reports
- Get detailed information about a specific person's report status
- View submission statistics
- Get a list of all team members who should submit reports

## Prerequisites

- Python 3.10 or higher
- A Google Sheets service account JSON file (`service_account.json`)
- Access to the "週報" Google Sheet

## Installation

```bash
# Install the package
pip install -e .

# Install in Claude Desktop
./install_server.sh
# or
mcp install mcp_server.main --name "週報檢查器"
```

## Usage

```bash
# Run in development mode
./run_server.sh
# or
mcp dev mcp_server.main

# Run directly
python -m mcp_server.main
# or
weekly-report-server
```

## Example Client

Run the example client:

```bash
python example_usage.py
```

## API Reference

### Resources

- `weekly-report://status` - Get who hasn't submitted reports
- `weekly-report://stats` - Get submission statistics
- `weekly-report://all-members` - Get all team members
- `weekly-report://person/{name}` - Get a specific person's status

### Tools

- `check_missing_reports` - Check missing reports
- `check_person_report` - Check a specific person's report
- `get_submission_stats` - Get submission statistics
```