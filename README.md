# VoidCode

A lightweight AI coding agent that runs in your terminal.It can read/write files and execute shell commands autonomously through an agent loop.

## Features

- **Agent Loop** — iteratively converses with the LLM until the task is complete
- **Read Tool** — reads file contents and feeds them to the model
- **Write Tool** — creates or overwrites files as instructed by the model
- **Bash Tool** — executes arbitrary shell commands and captures output

## Project Structure

```
app/
├── __init__.py   # Package marker
├── client.py     # OpenRouter API client setup
├── main.py       # Entry-point & agent loop
└── tools.py      # Tool schemas, implementations & dispatcher
```

## Setup

### Prerequisites

- Python 3.14+
- [uv](https://github.com/astral-sh/uv) package manager
- An [OpenRouter](https://openrouter.ai/) API key

### Installation

```bash
git clone https://github.com/<your-username>/VoidCode.git
cd VoidCode
uv sync
```

### Configuration

Create a `.env` file in the project root:

```
OPENROUTER_API_KEY=sk-or-v1-...
```

Or export the variable directly:

```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
```

## Usage

```bash
uv run -m app.main -p "your prompt here"
```

### Examples

```bash
# Read a file
uv run -m app.main -p "What is the content of README.md?"

# Create a file
uv run -m app.main -p "Create a hello.py that prints Hello World"

# Run a command
uv run -m app.main -p "List all Python files in the current directory"

# Multi-step task
uv run -m app.main -p "Read main.py, find any bugs, and fix them"
```

## How It Works

1. Your prompt is sent to the LLM along with available tool definitions
2. If the LLM requests tool calls, the agent executes them and returns results
3. The conversation continues until the LLM produces a final text response
4. The final answer is printed to stdout
