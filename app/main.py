"""Entry-point for the AI coding assistant."""

import argparse

from app.client import create_client, MODEL
from app.tools import TOOLS, execute_tool_call


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AI coding assistant")
    parser.add_argument("-p", dest="prompt", required=True, help="User prompt")
    return parser.parse_args()


def run(prompt: str) -> None:
    client = create_client()
    messages: list[dict] = [{"role": "user", "content": prompt}]

    while True:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
        )

        if not response.choices:
            raise RuntimeError("No choices in API response")

        message = response.choices[0].message

        # Append the assistant's response to conversation history.
        messages.append(message.model_dump())

        # If no tool calls, we have the final answer.
        if not message.tool_calls:
            print(message.content)
            break

        # Execute each requested tool and feed results back.
        for tool_call in message.tool_calls:
            result = execute_tool_call(tool_call)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })


def main() -> None:
    args = parse_args()
    run(args.prompt)


if __name__ == "__main__":
    main()
