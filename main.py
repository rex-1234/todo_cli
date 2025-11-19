"""CLI entrypoint for the to-do application using argparse subcommands."""
import argparse
import asyncio
from task_manager import TaskManager


async def main():
    """Parse CLI arguments and dispatch to task operations."""
    parser = argparse.ArgumentParser(description="Async To-do manager")
    sub = parser.add_subparsers(dest="command")

    # ADD
    p_add = sub.add_parser("add")
    p_add.add_argument("--title", required=True)
    p_add.add_argument("--due-date", required=True)

    # ADD MULTIPLE (TaskGroup)
    p_many = sub.add_parser("add-many")
    p_many.add_argument("--items", nargs="+", required=True)
    # Format: "title,2024-12-01" "Study,2024-01-10"

    # LIST
    sub.add_parser("list")

    # DELETE ONE
    p_del = sub.add_parser("delete")
    p_del.add_argument("--title", required=True)

    # DELETE MULTIPLE
    p_del_many = sub.add_parser("delete-many")
    p_del_many.add_argument("--titles", nargs="+", required=True)

    args = parser.parse_args()
    manager = TaskManager()

    try:
        async with asyncio.TaskGroup() as tg:

            # ADD
            if args.command == "add":
                tg.create_task(manager.add_tasks(args.title, args.due_date))

            # ADD MANY
            elif args.command == "add-many":
                for item in args.items:
                    title, date = item.split(",", 1)
                    tg.create_task(manager.add_tasks(title, date))

            # LIST
            elif args.command == "list":
                tg.create_task(manager.list_tasks())

            # DELETE
            elif args.command == "delete":
                tg.create_task(manager.delete_task(args.title))

            # DELETE MANY
            elif args.command == "delete-many":
                for title in args.titles:
                    tg.create_task(manager.delete_task(title))

            else:
                parser.print_help()

    except Exception as e:
        print(f"Error in TaskGroup: {e}")


if __name__ == "__main__":
    asyncio.run(main())
