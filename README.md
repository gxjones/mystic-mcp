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
from mystic_mcp import MysticServer

server = MysticServer("my-awesome-server", "1.0.0")

@server.tool("calculate")
async def calculate(expression: str) -> str:
    """Evaluate mathematical expressions safely."""
    # Your calculation logic here
    return str(eval(expression))  # Don't actually use eval() in production!

@server.resource("weather/{city}")
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

### Custom Resource Handlers

```python
@server.resource("files/{path}")
async def read_file(path: str, mime_type: str = "text/plain") -> bytes:
    """Read files from the filesystem."""
    with open(path, 'rb') as f:
        return f.read()
```

### Tool with Complex Parameters

```python
from typing import List, Optional

@server.tool("search")
async def search_documents(
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
server = MysticServer(
    name="my-server",
    version="1.0.0",
    description="An awesome MCP server",
    author="Your Name",
    license="MIT"
)

# Configure logging
server.configure_logging(level="INFO", format="json")

# Add middleware
server.add_middleware(cors=True, rate_limiting=True)
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

## Project Structure

```
your-mcp-server/
├── server.py              # Your main server file
├── tools/                 # Tool implementations
│   ├── __init__.py
│   ├── calculator.py
│   └── weather.py
├── resources/             # Resource handlers
│   ├── __init__.py
│   └── files.py
├── requirements.txt       # Dependencies
└── README.md             # Your server documentation
```

## Best Practices

- **One responsibility per tool/resource**: Keep functions focused and single-purpose
- **Use type hints**: Enable better IDE support and runtime validation
- **Handle errors gracefully**: Use try/catch blocks and return meaningful error messages
- **Document your tools**: Write clear docstrings for auto-generated help
- **Test thoroughly**: Write unit tests for your tools and resources

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

Licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.

## Links

- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [Documentation](https://mystic-mcp.readthedocs.io/)
- [Examples](https://github.com/gxjones/mystic-mcp/tree/main/examples)
- [Issues](https://github.com/gxjones/mystic-mcp/issues)
