# Expense Tracker MCP Server

A Model Context Protocol (MCP) server for tracking personal expenses with Claude. This server provides tools for adding, editing, deleting, searching, and summarizing expenses through a SQLite database.

## Features

- **Add Expenses**: Record expenses with date, amount, category, subcategory, and notes
- **List Expenses**: View expenses within a date range
- **Edit Expenses**: Update any field of an existing expense
- **Delete Expenses**: Remove expense entries by ID
- **Search Expenses**: Find expenses by keyword across categories and notes
- **Summarize**: Get spending summaries by category for any date range
- **Natural Language**: Use conversational commands with Claude (e.g., "add a trip to New York $500 last week")

## Prerequisites

- Python 3.8 or higher
- Claude Desktop app
- `uv` package manager

## Installation

### 1. Install UV Package Manager
```bash
pip install uv
```

### 2. Set Up Project

Navigate to your project folder and initialize:
```bash
cd /path/to/expense-tracker
uv init .
```

### 3. Install Dependencies
```bash
uv add fastmcp
```

## Testing the Server

### Using MCP Inspector

Test your server in the browser-based inspector:
```bash
uv run fastmcp dev main.py
```

This opens a web interface where you can test all the tools.

### Running the Server Standalone
```bash
uv run fastmcp run main.py
```

## Connecting to Claude Desktop

### 1. Install to Claude Desktop
```bash
uv run fastmcp install claude-desktop main.py
```

### 2. Update Configuration

Find the full path to your `uv` executable:
```bash
which uv  # On macOS/Linux
where uv  # On Windows
```

Open Claude Desktop settings:
`Settings > Developer > Edit Config`

Replace the `command` field from `"uv"` to the actual path:

### 3. Restart Claude Desktop

Completely quit and restart Claude Desktop for the changes to take effect.

## Usage Examples

Once connected to Claude Desktop, you can use natural language commands:

'''
Add a new expense: trip to New York $500 last week Monday to Saturday
Show me all expenses from last month
Delete the flight to new york expense on 24 november 2024 from the database
'''

## Project Structure
```
expense-tracker/
├── main.py              # MCP server code
├── categories.json      # Expense categories
├── expenses.db          # SQLite database (created automatically)
├── pyproject.toml       # UV project configuration
└── README.md            # This file
```

## Troubleshooting

### Server Not Showing in Claude

1. Verify the `uv` path is correct in the config
2. Check that the path to `main.py` is absolute
3. Restart Claude Desktop completely
4. Check Claude Desktop logs for errors

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.
