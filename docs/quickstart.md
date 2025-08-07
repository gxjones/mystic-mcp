# Quick Start Guide

This guide will help you get started with Mystic MCP quickly.

## Installation

Install Mystic MCP using pip:

```bash
pip install mystic-mcp
```

## Your First MCP Server

Create a simple MCP server in just a few lines:

```python
from mystic_mcp import MysticMCP

app = MysticMCP()

@app.tool()
async def hello_world(name: str = "World"):
    """Say hello to someone
    
    Args:
        name: The name to greet
    """
    return f"Hello, {name}!"

if __name__ == "__main__":
    app.run()
```

Save this as `hello_server.py` and run it:

```bash
python hello_server.py
```

Your server will start on `http://127.0.0.1:5000`.

## Understanding Tools

Tools are functions that your MCP server exposes. They are registered using the `@app.tool()` decorator.

### Tool Requirements

1. **Function signature**: The function parameters become the tool's input schema
2. **Type hints**: Used to generate JSON schema validation
3. **Docstring**: Provides the tool's description

### Supported Types

Mystic MCP supports all standard Python types and generates appropriate JSON schemas:

```python
from typing import Literal, Optional, List
from mystic_mcp import MysticMCP

app = MysticMCP()

@app.tool()
async def complex_tool(
    text: str,
    count: int = 1,
    category: Literal["info", "warning", "error"] = "info",
    tags: Optional[List[str]] = None
):
    """A tool with various parameter types
    
    Args:
        text: The message text
        count: How many times to repeat
        category: Message category
        tags: Optional list of tags
    """
    result = f"[{category.upper()}] {text}"
    if tags:
        result += f" (tags: {', '.join(tags)})"
    
    return "\n".join([result] * count)
```

This generates a comprehensive JSON schema with:
- Required vs optional parameters
- Type validation (string, integer, enum)
- Default values
- Array support

## Running Your Server

### Development Server

For development, use the built-in server:

```python
app.run(host="127.0.0.1", port=5000, backend="wsgiref")
```

### Production Deployment

For production, you can use different backends:

```python
# Using Uvicorn (ASGI)
app.run(backend="uvicorn", host="0.0.0.0", port=8000)

# Using Waitress (WSGI)
app.run(backend="waitress", host="0.0.0.0", port=8000)
```

Or deploy with your preferred WSGI/ASGI server:

```python
# For WSGI servers like Gunicorn
from myapp import app
# app is callable as WSGI application

# For ASGI servers like Uvicorn
from myapp import app
# Use app.asgi_app for ASGI
```

## Configuration

You can configure your MCP server:

```python
config = {
    "debug": True,
    "cors_enabled": True,
}

app = MysticMCP(config=config)
```

## Next Steps

- Check out the [API Reference](api.md) for detailed documentation
- See [Examples](examples.md) for more complex use cases
- Learn about advanced features like custom validation and middleware
