"""CLI entrypoint for the to-do application using argparse subcommands."""
import argparse
from json import JSONDecodeError
from task_manager import TaskManager

def main():
    """Parse CLI arguments and dispatch to task operations."""
    parser = argparse.ArgumentParser(description="Simple To-do list manager")
    subparsers = parser.add_subparsers(dest="command", help="Command")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("--title", required=True, help="Task title")
    add_parser.add_argument("--due-date", required=True, help="Task due date in YYYY-MM-DD format")

    # List command
    subparsers.add_parser("list", help="List all tasks")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("--title", required=True, help="Task title to delete")

    args = parser.parse_args()
    manager = TaskManager()

    try:
        if args.command == "add":
            manager.add_tasks(args.title, args.due_date)
        elif args.command == "list":
            manager.list_tasks()
        elif args.command == "delete":
            manager.delete_task(args.title)
        else:
            parser.print_help()
    except (ValueError, JSONDecodeError, OSError) as e:
        print(f"CLI error: {e}")

if __name__ == "__main__":
    main()
