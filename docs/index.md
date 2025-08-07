# Mystic MCP

A Python framework for building Model Context Protocol (MCP) servers with automatic JSON schema generation.

```{toctree}
:maxdepth: 2
:caption: Contents:

quickstart
api
examples
```

## Overview

Mystic MCP simplifies creating MCP servers by providing:

- **Automatic Schema Generation**: Uses Pydantic to generate JSON schemas from Python type hints
- **Decorator-based Tool Registration**: Simple `@app.tool()` decorator for registering functions
- **Type Safety**: Full support for Python typing including `Literal`, `Optional`, and complex types
- **Multiple Server Backends**: Support for WSGI, ASGI, and various web servers

## Quick Example

```python
from mystic_mcp import MysticMCP
from typing import Literal

app = MysticMCP()

PIZZA_TYPES = Literal["margherita", "pepperoni", "veggie"]

@app.tool()
async def order_pizza(pizza_type: PIZZA_TYPES, customer_name: str = "Customer"):
    """Order a pizza
    
    Args:
        pizza_type: Type of pizza to order
        customer_name: Name for the order
    """
    return f"Ordered {pizza_type} pizza for {customer_name}"

if __name__ == "__main__":
    app.run()
```

This automatically generates proper JSON schemas:

```json
{
  "type": "object",
  "properties": {
    "pizza_type": {
      "type": "string",
      "enum": ["margherita", "pepperoni", "veggie"]
    },
    "customer_name": {
      "type": "string",
      "default": "Customer"
    }
  },
  "required": ["pizza_type"]
}
```

## Installation

```bash
pip install mystic-mcp
```

## Indices and tables

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`
