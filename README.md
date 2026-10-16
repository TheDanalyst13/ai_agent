# AI Agent: A Command-Line Coding Agent in Python

## Project Status
**Complete (v1)** — the core agent loop works: it takes a prompt, decides which tools to call, executes them, and iterates until it has an answer. Possible extensions are listed in the roadmap below.

## Overview
A command-line AI agent built with Python and the [OpenRouter](https://openrouter.ai) API. Given a plain-English task, the agent can explore a project directory, read and write files, and run Python scripts, calling these functions on its own and feeding the results back to the model until the task is done. In testing, it was pointed at a small calculator app to find and fix bugs.

> Built as part of the [Boot.dev](https://www.boot.dev) backend development curriculum. This is a guided learning project, not an original design. Its purpose was to practice working with LLM APIs, function calling, and agentic loops.

## How it works
1. The user passes a prompt on the command line
2. The prompt is sent to an LLM (via OpenRouter) along with a list of available tools
3. If the model requests a tool call, the program executes the function and returns the result to the model
4. The loop repeats until the model produces a final response (or hits an iteration limit)

## Available Tools
| Function | What it does |
|---|---|
| `get_files_info` | Lists files and directories, with sizes |
| `get_file_content` | Reads the contents of a file |
| `write_file` | Creates or overwrites a file |
| `run_python_file` | Executes a Python file and returns its output |

## Safety Constraints
Because the agent can write and execute code, its file access is limited:
- All paths are validated and restricted to a single permitted working directory
- Attempts to access paths outside that directory are rejected
- File reads are truncated at a maximum length
- Script execution has a timeout

This is a learning project, so it is **not hardened for untrusted use**. Don't point it at directories containing anything sensitive.

## Tools & Methods
- **Python** — core language
- **OpenRouter API** — unified access to LLMs, with tool/function calling support
- **uv** — dependency and environment management
- **python-dotenv** — loading the API key from a `.env` file
- Agentic loop design, function declarations/schemas, and path-validation for sandboxing

## What I Practiced
- Calling an LLM API through OpenRouter and handling structured responses
- Defining tool schemas so a model can call functions
- Building a feedback loop where tool results inform the next model call
- Securing file access with path validation and execution limits
- Managing secrets with environment variables

## How to Run
**Requirements:** Python 3, [uv](https://docs.astral.sh/uv/), and an [OpenRouter API key](https://openrouter.ai/keys)

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai_agent.git
   cd ai_agent
   ```
2. Create a `.env` file in the project root:
   ```
   OPENROUTER_API_KEY=your_key_here
   ```
3. Run the agent with a prompt:
   ```bash
   uv run main.py "your prompt here"
   ```
   Add `--verbose` to see token usage and each tool call.

## Next Steps / Roadmap
- Add support for deleting or renaming files (with confirmation)
- Add conversation memory across runs
- Experiment with additional tools (e.g., searching file contents)
- Compare behavior across different models available through OpenRouter
- Add automated tests for the file-access functions

## Repo Structure
```
├── main.py            # entry point and agent loop
├── prompts.py         # system prompt
├── config.py          # constants (limits, working directory)
├── call_function.py   # dispatches model tool calls to functions
├── functions/         # tool implementations
├── calculator/        # sample project the agent works on
├── pyproject.toml     # project metadata and dependencies
├── .gitignore         # excludes .env and other local files
└── README.md
```
