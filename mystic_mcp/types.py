import ast
from typing import Annotated, Any, Callable, TypedDict


class Tool(TypedDict):
    name: str
    description: str
    inputSchema: dict  # JSON schema for input parameters
    outputSchema: dict  # JSON schema for output
    func: Callable
    source_name: str
    func_doc: str
