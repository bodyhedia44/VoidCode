import argparse
import sys

from app.client import create_client, MODEL
from app.tools import TOOLS, execute_tool_call


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AI coding assistant")
    parser.add_argument("-p", dest="prompt", required=True, help="User prompt")
    return parser.parse_args()


def run(prompt: str) -> None:
    client = create_client()

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        tools=TOOLS,
    )

    if not response.choices:
        raise RuntimeError("No choices in API response")

    message = response.choices[0].message

    # If the model requested tool calls, execute the first one and print the result.
    if message.tool_calls:
        result = execute_tool_call(message.tool_calls[0])
        print(result, end="")
    else:
        # No tool call — just print the text reply.
        print(message.content)


def main() -> None:
    args = parse_args()
    run(args.prompt)


if __name__ == "__main__":
    main()
