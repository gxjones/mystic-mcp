# API Reference

Complete API documentation for Mystic MCP.

## Core Classes

```{eval-rst}
.. automodule:: mystic_mcp.core
   :members:
   :undoc-members:
   :show-inheritance:
```

## Type Definitions

```{eval-rst}
.. automodule:: mystic_mcp.types
   :members:
   :undoc-members:
   :show-inheritance:
```

## Utility Functions

```{eval-rst}
.. automodule:: mystic_mcp.ast_utils
   :members:
   :undoc-members:
   :show-inheritance:
```

## MysticMCP Class

The main class for creating MCP servers.

### Constructor

```python
MysticMCP(config: dict = None)
```

Creates a new MCP server instance.

**Parameters:**
- `config` (dict, optional): Configuration dictionary for the server

### Methods

#### tool(name: str = None)

Decorator for registering tool functions.

**Parameters:**
- `name` (str, optional): Custom name for the tool. If not provided, uses the function name.

**Returns:**
- Decorator function that registers the tool

**Example:**
```python
@app.tool()
async def my_tool(param: str):
    """Tool description"""
    return f"Result: {param}"

@app.tool("custom_name")
async def another_tool():
    """Tool with custom name"""
    return "Hello"
```

#### run(host: str = "127.0.0.1", port: int = 5000, backend: str = "wsgiref")

Starts the MCP server.

**Parameters:**
- `host` (str): Host address to bind to
- `port` (int): Port number to listen on  
- `backend` (str): Server backend to use. Options:
  - `"wsgiref"`: Python built-in WSGI server (development)
  - `"uvicorn"`: ASGI server (production)
  - `"waitress"`: WSGI server (production)
  - `"werkzeug"`: Development WSGI server
  - `"hypercorn"`: ASGI server

**Example:**
```python
# Development
app.run()

# Production with Uvicorn
app.run(host="0.0.0.0", port=8000, backend="uvicorn")
```

### Properties

#### tools

Dictionary of registered tools.

**Type:** `dict[str, Tool]`

**Example:**
```python
# Access registered tools
for name, tool in app.tools.items():
    print(f"Tool: {name}")
    print(f"Schema: {tool['inputSchema']}")
```

## Tool Type

The `Tool` type represents a registered tool function.

```python
class Tool(TypedDict):
    name: str                    # Tool name
    description: str             # Tool description from docstring
    inputSchema: dict           # JSON schema for input parameters
    outputSchema: dict          # JSON schema for output
    func: Callable              # The actual function
    source_name: str            # Source file and line number
    func_doc: str               # Function docstring
```

## Schema Generation

Mystic MCP automatically generates JSON schemas from Python type hints:

### Supported Types

| Python Type | JSON Schema |
|-------------|-------------|
| `str` | `{"type": "string"}` |
| `int` | `{"type": "integer"}` |
| `float` | `{"type": "number"}` |
| `bool` | `{"type": "boolean"}` |
| `list` | `{"type": "array"}` |
| `dict` | `{"type": "object"}` |
| `Literal["a", "b"]` | `{"type": "string", "enum": ["a", "b"]}` |
| `Optional[str]` | `{"type": "string", "nullable": true}` |
| `List[str]` | `{"type": "array", "items": {"type": "string"}}` |

### Parameter Handling

- **Required parameters**: Parameters without default values
- **Optional parameters**: Parameters with default values (not in `required` array)
- **Default values**: Included in the schema for documentation

### Example Schema Generation

```python
from typing import Literal, List, Optional

@app.tool()
async def example_tool(
    name: str,
    age: int = 25,
    role: Literal["admin", "user"] = "user",
    skills: Optional[List[str]] = None
):
    """Example tool with various parameter types"""
    pass
```

Generates:

```json
{
  "type": "object",
  "properties": {
    "name": {"type": "string"},
    "age": {"type": "integer", "default": 25},
    "role": {
      "type": "string", 
      "enum": ["admin", "user"], 
      "default": "user"
    },
    "skills": {
      "type": "array",
      "items": {"type": "string"},
      "nullable": true,
      "default": null
    }
  },
  "required": ["name"]
}
```
