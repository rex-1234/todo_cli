# To-Do CLI

Simple command-line task manager that stores tasks in a JSON file and logs operations to rotating log files.

## Prerequisites
- Python 3.10 or later
- `pip` for installing dependencies (standard library only by default)

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

## Usage
Run the CLI from the project root:

```bash
python3 main.py <command> [options]
```

### Commands
- `add` — create a task  
  `python3 main.py add --title "Buy milk" --due-date 2025-11-15`
- `list` — display all tasks with overdue status  
  `python3 main.py list`
- `delete` — remove a task by title  
  `python3 main.py delete --title "Buy milk"`

## Data & Logs
- Tasks persist in `tasks.json`. You can back up or edit this file manually if needed.
- Logs rotate under `logs/todo.log`, keeping the most recent logs for 5 days and maximum size of 100 KB.

## Testing
No automated tests yet. Run commands manually and check `logs/todo.log` for issues.

## Contributing
1. Fork and clone the repo.
2. Create a branch for your change.
3. Submit a pull request with a description and testing notes.


