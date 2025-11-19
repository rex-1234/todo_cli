# To-Do CLI

Simple command-line task manager that stores tasks in a JSON file and logs operations to rotating log files.

## Prerequisites

- Python 3.13 or later (matches `pyproject.toml`)
- One of:
  - [uv](https://github.com/astral-sh/uv) for dependency management (recommended)
  - Standard `python3` + `pip`

## Setup

### Option A: uv (recommended)

```bash
# 1. Install uv if you don't already have it (see uv docs)
# 2. Sync dependencies and create .venv automatically
uv sync

# 3. (Optional) activate the environment
source .venv/bin/activate
```

### Option B: python3 + pip

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
```

## Usage

Run the CLI from the project root:

```bash
# with the system interpreter
python3 main.py <command> [options]

# or, using uv
uv run python main.py <command> [options]
```

### Commands

| Command       | Description                                                   | Example                                                                               |
| ------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `add`         | Create a single task                                          | `python3 main.py add --title "Learn Python" --due-date 2025-11-20`                    |
| `add-many`    | Create multiple tasks in parallel (format `title,YYYY-MM-DD`) | `python3 main.py add-many --items "Learn Flask,2025-11-25" "Learn Devops,2025-11-20"` |
| `list`        | Display all tasks with overdue status                         | `python3 main.py list`                                                                |
| `delete`      | Remove a single task                                          | `python3 main.py delete --title "Learn Python"`                                       |
| `delete-many` | Remove several tasks at once                                  | `python3 main.py delete-many --titles "Learn Flask" "Learn Devops"`                   |

> Tip: Replace `python3` with `uv run python` if you’re using uv.

## Data & Logs

- Tasks persist in `tasks.json`. You can back up or edit this file manually if needed.
- Logs rotate under `logs/todo.log`, keeping the most recent logs for 5 days and maximum size of 100 KB.

## Testing

No automated tests yet. Run commands manually and check `logs/todo.log` for issues.

## Contributing

1. Fork and clone the repo.
2. Create a branch for your change.
3. Submit a pull request with a description and testing notes.
