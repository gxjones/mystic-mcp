"""
Core functionality for Mystic MCP.
"""

import asyncio
from inspect import iscoroutinefunction
from pprint import pprint
from typing import Callable

from mystic_mcp.ast_utils import extract_function_schemas
from mystic_mcp.types import Tool


class MysticMCP:
    def __init__(self, config=None):
        """Initialize MysticMCP instance.

        Args:
            config (dict, optional): Configuration dictionary.
        """
        self.config = config or {}
        self.tools: dict[str, Tool] = {}

    def tool(self, name: str = None):
        def decorator(func: Callable):
            description = func.__doc__
            tool_name = name if name is not None else func.__name__

            # Extract schemas using Pydantic
            schemas = extract_function_schemas(func)

            self.tools[tool_name] = tool = Tool(
                name=tool_name,
                description=description,
                inputSchema=schemas["inputSchema"],
                outputSchema=schemas["outputSchema"],
                func=func,
                source_name=f"{func.__code__.co_filename}:{func.__code__.co_firstlineno}",
                func_doc=func.__doc__,
            )
            pprint(tool)
            return func

        return decorator

    def __call__(self, environ, start_response):
        """
        WSGI interface
        """
        path = environ.get("PATH_INFO", "/")
        handler = self.tools.get(path)

        if handler:
            if iscoroutinefunction(handler):
                response_body = asyncio.run(handler())
            else:
                response_body = handler()
            status = "200 OK"
        else:
            response_body = "Not Found"
            status = "404 Not Found"

        response_headers = [
            ("Content-Type", "text/plain"),
            ("Content-Length", str(len(response_body.encode()))),
        ]
        start_response(status, response_headers)
        return [response_body.encode()]

    # ASGI interface
    async def asgi_app(self, scope, receive, send):
        """
        ASGI interface
        """
        assert scope["type"] == "http"
        path = scope["path"]
        handler = self.tools.get(path)

        if handler:
            if iscoroutinefunction(handler):
                response_body = await handler()
            else:
                response_body = handler()
            status = 200
        else:
            response_body = "Not Found"
            status = 404

        await send(
            {
                "type": "http.response.start",
                "status": status,
                "headers": [
                    (b"content-type", b"text/plain"),
                    (b"content-length", str(len(response_body.encode())).encode()),
                ],
            }
        )

        await send(
            {
                "type": "http.response.body",
                "body": response_body.encode(),
            }
        )

    def run(self, host="127.0.0.1", port=5000, backend="wsgiref"):
        print(f"Starting server on http://{host}:{port} using {backend}...")
        if backend == "wsgiref":
            from wsgiref.simple_server import make_server

            with make_server(host, port, self) as httpd:
                httpd.serve_forever()
        elif backend == "werkzeug":
            from werkzeug.serving import run_simple

            run_simple(host, port, self)
        elif backend == "waitress":
            import waitress

            waitress.serve(self, host=host, port=port)
        elif backend == "uvicorn":
            import uvicorn

            uvicorn.run(self.asgi_app, host=host, port=port)
        elif backend == "hypercorn":
            import asyncio

            from hypercorn.asyncio import serve
            from hypercorn.config import Config

            config = Config()
            config.bind = [f"{host}:{port}"]
            asyncio.run(serve(self.asgi_app, config))
        else:
            raise ValueError(f"Unsupported backend: {backend}")
