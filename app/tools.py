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
},
{
    "type": "function",
    "function": {
        "name": "Write",
        "description": "Write content to a file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the file to write to",
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the file",
                },
            },
            "required": ["file_path", "content"],
        },
    },
},
]

def execute_read(file_path: str) -> str:
    """Read a file and return its contents."""
    with open(file_path, "r") as f:
        return f.read()


def execute_write(file_path: str, content: str) -> str:
    """Write content to a file, creating or overwriting it."""
    with open(file_path, "w") as f:
        f.write(content)
    return f"Successfully wrote to {file_path}"


# -- Dispatcher --------------------------------------------------------------------

TOOL_REGISTRY: dict[str, callable] = {
    "Read": lambda args: execute_read(args["file_path"]),
    "Write": lambda args: execute_write(args["file_path"], args["content"]),
}


def execute_tool_call(tool_call) -> str:
    """Parse and execute a single tool call, returning the result string."""
    name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)

    handler = TOOL_REGISTRY.get(name)
    if handler is None:
        raise RuntimeError(f"Unknown tool: {name}")

    return handler(arguments)
