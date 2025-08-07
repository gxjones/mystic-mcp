"""
Type utilities for function analysis and JSON schema generation.
"""

import inspect
from typing import Callable, get_type_hints, get_origin, get_args
from pydantic import TypeAdapter, create_model
from pydantic.fields import FieldInfo


def extract_function_schemas(func: Callable) -> dict:
    """Extract JSON schemas for function parameters and return type using Pydantic.
    
    Args:
        func: The function to analyze
        
    Returns:
        Dictionary with inputSchema and outputSchema
    """
    # Get function signature and type hints
    sig = inspect.signature(func)
    type_hints = get_type_hints(func)
    
    # Build fields for input schema
    fields = {}
    for param_name, param in sig.parameters.items():
        # Get type from type hints or annotation
        param_type = type_hints.get(param_name, param.annotation)
        if param_type == inspect.Parameter.empty:
            param_type = str  # Default to string
        
        # Determine if parameter is required
        if param.default == inspect.Parameter.empty:
            # Required parameter
            fields[param_name] = (param_type, FieldInfo())
        else:
            # Optional parameter with default
            fields[param_name] = (param_type, FieldInfo(default=param.default))
    
    # Create input schema using Pydantic
    if fields:
        InputModel = create_model('InputSchema', **fields)
        input_schema = InputModel.model_json_schema()
    else:
        input_schema = {"type": "object", "properties": {}}
    
    # Create output schema
    return_type = type_hints.get('return', str)
    if return_type == inspect.Signature.empty:
        return_type = str
    
    try:
        output_adapter = TypeAdapter(return_type)
        output_schema = output_adapter.json_schema()
    except Exception:
        # Fallback for complex types
        output_schema = {"type": "string"}
    
    return {
        "inputSchema": input_schema,
        "outputSchema": output_schema
    }
