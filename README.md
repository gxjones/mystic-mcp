# Mystic MCP
![mysticmcp](docs/assets/AD85F741-E621-4DE7-876B-F6984A68E35A.png)

A high-level Python framework for building Model Context Protocol (MCP) servers without the complexity.

## What is MCP?

The [Model Context Protocol](https://modelcontextprotocol.io/) is an open standard that enables AI assistants to securely connect to external data sources and tools. MCP servers expose resources, tools, and prompts that AI models can use to enhance their capabilities.

## Why Mystic MCP?

Building MCP servers from scratch involves handling protocol details, connection management, and complex async patterns. Mystic MCP abstracts these complexities so you can focus on your server's functionality.

**Perfect for "vibe coders" who want to:**
- Build MCP servers without protocol expertise
- Focus on business logic, not boilerplate
- Get from idea to working server quickly
- Handle async operations seamlessly

## Installation

```bash
pip install mystic-mcp
```

## Quick Start

```python
from mystic_mcp import MysticMCP

server = MysticMCP("my-awesome-server", "1.0.0")

@server.tool()
async def calculate(expression: str) -> str:
    """Evaluate mathematical expressions safely."""
    # Your calculation logic here
    return str(eval(expression))  # Don't actually use eval() in production!

@server.tool()
async def get_weather(city: str) -> dict:
    """Get weather data for a city."""
    # Your weather API integration here
    return {"city": city, "temperature": "22°C", "condition": "sunny"}

if __name__ == "__main__":
    server.run()
```

## Features

- **Decorators for everything**: Simple `@server.tool()` and `@server.resource()` decorators
- **Async by default**: Built-in async/await support with proper error handling
- **Type safety**: Full typing support with runtime validation
- **Auto-discovery**: Automatic resource and tool registration
- **Development server**: Built-in dev server with hot reload
- **Logging**: Structured logging with configurable levels
- **Validation**: Request/response validation with helpful error messages

## Advanced Usage


### Tool with Complex Parameters

```python
from typing import List, Optional

@server.tool()
async def search(
    query: str,
    filters: Optional[List[str]] = None,
    limit: int = 10
) -> List[dict]:
    """Search through document collection."""
    # Your search implementation
    return []
```

### Server Configuration

```python
server = MysticMCP(
    name="my-server",
    version="1.0.0",
    description="An awesome MCP server",
    author="Your Name",
    license="MIT"
)

```

## Development

```bash
# Clone the repository
git clone https://github.com/gxjones/mystic-mcp.git
cd mystic-mcp

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with hot reload
mystic-mcp dev your_server.py
```

### Code Quality

This project uses modern Python tooling for code quality and consistency:

```bash
# Format code (auto-fixes style issues)
ruff format .

# Lint and auto-fix common issues
ruff check --fix .

# Type checking
mypy mystic_mcp/

# Run all quality checks
ruff check . && ruff format --check . && mypy mystic_mcp/
```

**Tools used:**
- **Ruff**: Fast linting and formatting (replaces Black, Flake8, isort)
- **mypy**: Static type checking
- Configuration in `pyproject.toml`

**IDE Setup:**
- Install the Ruff extension for your editor (VS Code, PyCharm, etc.)
- Enable format-on-save for automatic code formatting
- Most editors will show linting errors inline

**Pre-commit hooks** (optional but recommended):
```bash
pip install pre-commit
pre-commit install
```

This ensures code is automatically formatted and linted before each commit.

## License

Licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.

## Links

- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [Documentation](https://mystic-mcp.readthedocs.io/)
- [Examples](https://github.com/gxjones/mystic-mcp/tree/main/examples)
- [Issues](https://github.com/gxjones/mystic-mcp/issues)
