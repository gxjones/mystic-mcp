# Examples

Real-world examples of using Mystic MCP.

## Pizza Ordering Server

A complete example showing a pizza ordering system with multiple tools and complex types.

```python
#!/usr/bin/env python3
"""
A Pizza MCP Server
Minimal example using the mystic-mcp framework
"""

from mystic_mcp import MysticMCP
from typing import Literal

app = MysticMCP()

# Simple pizza data
PIZZA_TYPES = Literal["margherita", "pepperoni", "veggie"]
MENU = {
    "margherita": {"name": "Margherita", "price": 12.99},
    "pepperoni": {"name": "Pepperoni", "price": 15.99},
    "veggie": {"name": "Veggie Deluxe", "price": 14.99},
}

ORDERS = {}

@app.tool()
async def get_menu():
    """Get the pizza menu"""
    result = "MENU:\n"
    for _pizza_id, info in MENU.items():
        result += f"- {info['name']}: ${info['price']}\n"
    return result

@app.tool()
async def order_pizza(pizza_type: PIZZA_TYPES, customer_name: str = "Customer"):
    """Order a pizza"""
    if pizza_type not in MENU:
        return f"Sorry, we don't have {pizza_type}. Try: {', '.join(MENU.keys())}"

    order_id = f"order-{len(ORDERS) + 1}"
    pizza = MENU[pizza_type]

    ORDERS[order_id] = {
        "pizza": pizza["name"],
        "price": pizza["price"],
        "customer": customer_name,
        "status": "preparing",
    }

    return f"Order {order_id}: {pizza['name']} for {customer_name} - ${pizza['price']}"

@app.tool()
async def check_order(order_id: str):
    """Check order status

    Args:
        order_id: Your order ID
    """
    if order_id not in ORDERS:
        return f"Order {order_id} not found"

    order = ORDERS[order_id]
    return f"Order {order_id}: {order['pizza']} for {order['customer']} - Status: {order['status']}"

if __name__ == "__main__":
    print("Starting the pizza MCP server...")
    app.run()
```

### Generated Schemas

The pizza ordering server automatically generates these JSON schemas:

**get_menu tool:**
```json
{
  "type": "object",
  "properties": {}
}
```

**order_pizza tool:**
```json
{
  "type": "object",
  "properties": {
    "pizza_type": {
      "type": "string",
      "enum": ["margherita", "pepperoni", "veggie"],
      "title": "Pizza Type"
    },
    "customer_name": {
      "type": "string",
      "default": "Customer",
      "title": "Customer Name"
    }
  },
  "required": ["pizza_type"],
  "title": "InputSchema"
}
```

**check_order tool:**
```json
{
  "type": "object",
  "properties": {
    "order_id": {
      "type": "string",
      "title": "Order Id"
    }
  },
  "required": ["order_id"],
  "title": "InputSchema"
}
```

## File Operations Server

Example showing file operations with different parameter types:

```python
from mystic_mcp import MysticMCP
from typing import Literal, Optional, List
import os
import json

app = MysticMCP()

FileMode = Literal["read", "write", "append"]
FileFormat = Literal["text", "json", "binary"]

@app.tool()
async def read_file(
    filepath: str,
    format: FileFormat = "text",
    encoding: str = "utf-8"
):
    """Read a file with specified format
    
    Args:
        filepath: Path to the file to read
        format: Format to read the file as
        encoding: Text encoding to use
    """
    try:
        if format == "binary":
            with open(filepath, 'rb') as f:
                content = f.read()
            return f"Binary file read: {len(content)} bytes"
        
        with open(filepath, 'r', encoding=encoding) as f:
            content = f.read()
            
        if format == "json":
            parsed = json.loads(content)
            return {"type": "json", "data": parsed}
        
        return {"type": "text", "content": content}
    
    except Exception as e:
        return {"error": str(e)}

@app.tool()
async def write_file(
    filepath: str,
    content: str,
    mode: FileMode = "write",
    create_dirs: bool = False
):
    """Write content to a file
    
    Args:
        filepath: Path where to write the file
        content: Content to write
        mode: Write mode (write=overwrite, append=add to end)
        create_dirs: Whether to create parent directories
    """
    try:
        if create_dirs:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        file_mode = "w" if mode == "write" else "a"
        
        with open(filepath, file_mode) as f:
            f.write(content)
        
        return f"Successfully wrote to {filepath}"
    
    except Exception as e:
        return {"error": str(e)}

@app.tool()
async def list_directory(
    path: str = ".",
    include_hidden: bool = False,
    file_types: Optional[List[str]] = None
):
    """List files in a directory
    
    Args:
        path: Directory path to list
        include_hidden: Whether to include hidden files (starting with .)
        file_types: List of file extensions to filter by (e.g., [".py", ".txt"])
    """
    try:
        files = []
        for item in os.listdir(path):
            if not include_hidden and item.startswith('.'):
                continue
            
            if file_types:
                if not any(item.endswith(ext) for ext in file_types):
                    continue
            
            item_path = os.path.join(path, item)
            files.append({
                "name": item,
                "type": "directory" if os.path.isdir(item_path) else "file",
                "size": os.path.getsize(item_path) if os.path.isfile(item_path) else None
            })
        
        return {"path": path, "files": files}
    
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    app.run(port=5001)
```

## Task Management Server

Example with complex data structures and state management:

```python
from mystic_mcp import MysticMCP
from typing import Literal, Optional, List, Dict, Any
from datetime import datetime, timedelta
import uuid

app = MysticMCP()

TaskStatus = Literal["pending", "in_progress", "completed", "cancelled"]
TaskPriority = Literal["low", "medium", "high", "urgent"]

# In-memory task storage
TASKS: Dict[str, Dict[str, Any]] = {}

@app.tool()
async def create_task(
    title: str,
    description: str = "",
    priority: TaskPriority = "medium",
    due_date: Optional[str] = None,
    tags: Optional[List[str]] = None
):
    """Create a new task
    
    Args:
        title: Task title
        description: Detailed description
        priority: Task priority level
        due_date: Due date in ISO format (YYYY-MM-DD)
        tags: List of tags for categorization
    """
    task_id = str(uuid.uuid4())
    
    task = {
        "id": task_id,
        "title": title,
        "description": description,
        "priority": priority,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "due_date": due_date,
        "tags": tags or [],
        "completed_at": None
    }
    
    TASKS[task_id] = task
    
    return {
        "message": "Task created successfully",
        "task": task
    }

@app.tool()
async def update_task_status(
    task_id: str,
    status: TaskStatus
):
    """Update the status of a task
    
    Args:
        task_id: ID of the task to update
        status: New status for the task
    """
    if task_id not in TASKS:
        return {"error": f"Task {task_id} not found"}
    
    task = TASKS[task_id]
    old_status = task["status"]
    task["status"] = status
    
    if status == "completed":
        task["completed_at"] = datetime.now().isoformat()
    
    return {
        "message": f"Task status updated from {old_status} to {status}",
        "task": task
    }

@app.tool()
async def list_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    tag: Optional[str] = None
):
    """List tasks with optional filtering
    
    Args:
        status: Filter by task status
        priority: Filter by task priority  
        tag: Filter by tag (must contain this tag)
    """
    filtered_tasks = []
    
    for task in TASKS.values():
        # Apply filters
        if status and task["status"] != status:
            continue
        if priority and task["priority"] != priority:
            continue
        if tag and tag not in task["tags"]:
            continue
        
        filtered_tasks.append(task)
    
    # Sort by priority (urgent -> high -> medium -> low) then by created date
    priority_order = {"urgent": 0, "high": 1, "medium": 2, "low": 3}
    filtered_tasks.sort(
        key=lambda t: (priority_order[t["priority"]], t["created_at"])
    )
    
    return {
        "total": len(filtered_tasks),
        "tasks": filtered_tasks
    }

@app.tool()
async def get_task_stats():
    """Get task statistics"""
    if not TASKS:
        return {"message": "No tasks found"}
    
    stats = {
        "total": len(TASKS),
        "by_status": {},
        "by_priority": {},
        "overdue": 0
    }
    
    today = datetime.now().date()
    
    for task in TASKS.values():
        # Count by status
        status = task["status"]
        stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
        
        # Count by priority
        priority = task["priority"]
        stats["by_priority"][priority] = stats["by_priority"].get(priority, 0) + 1
        
        # Count overdue tasks
        if task["due_date"] and task["status"] != "completed":
            due = datetime.fromisoformat(task["due_date"]).date()
            if due < today:
                stats["overdue"] += 1
    
    return stats

if __name__ == "__main__":
    print("Starting task management MCP server...")
    app.run(port=5002)
```

## Running the Examples

Save any of these examples to a Python file and run them:

```bash
# Install dependencies
pip install mystic-mcp

# Run the pizza server
python pizza_server.py

# Run the file operations server  
python file_server.py

# Run the task management server
python task_server.py
```

Each server will start on a different port and provide its own set of tools with automatically generated JSON schemas.

## Key Takeaways

These examples demonstrate:

1. **Type Safety**: Using `Literal`, `Optional`, and `List` types for robust schemas
2. **Default Values**: Parameters with defaults become optional in the schema
3. **Complex Returns**: Returning dictionaries, lists, and nested data structures
4. **Error Handling**: Proper error responses in tools
5. **State Management**: Maintaining application state between tool calls
6. **Documentation**: Clear docstrings that become tool descriptions
