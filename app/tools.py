"""Tool definitions and execution logic."""

import json

# -- Tool schema sent to the LLM --------------------------------------------------

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "Read",
            "description": "Read and return the contents of a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The path to the file to read",
                    }
                },
                "required": ["file_path"],
            },
        },
    }
]

# -- Tool implementations ---------------------------------------------------------


def execute_read(file_path: str) -> str:
    """Read a file and return its contents."""
    with open(file_path, "r") as f:
        return f.read()


# -- Dispatcher --------------------------------------------------------------------

TOOL_REGISTRY: dict[str, callable] = {
    "Read": lambda args: execute_read(args["file_path"]),
}


def execute_tool_call(tool_call) -> str:
    """Parse and execute a single tool call, returning the result string."""
    name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)

    handler = TOOL_REGISTRY.get(name)
    if handler is None:
        raise RuntimeError(f"Unknown tool: {name}")

    return handler(arguments)
