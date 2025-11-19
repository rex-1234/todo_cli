"""Task management module: defines `Task` and `TaskManager` for a simple CLI."""

import json
import os
import asyncio
import aiofiles
import time
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from dataclasses import dataclass, field
from functools import wraps

# Ensure log directory exists
os.makedirs("logs", exist_ok=True)

# Create rotating file handler (SYNC Logic)
LOG_FILE = "logs/todo.log"
handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes = 1024 * 100,   # 100 KB per file
    backupCount = 5,         # Keep 5 old log files
    encoding = "utf-8"
)

# Define log format
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
handler.setFormatter(formatter)

#create logger and attach handler
logger = logging.getLogger("todo_logger")
logger.setLevel(logging.INFO)
if not logger.hasHandlers():
    logger.addHandler(handler)

# Async lock for safe file operations
file_lock = asyncio.Lock()


# --------------------------------------------------------
# ASYNC DECORATOR
# --------------------------------------------------------
def safe_operation(func):
    """Async decorator: handles errors, timing, and logging."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        try:
            result = await func(*args, **kwargs)
            logger.info(f"{func.__name__} executed successfully.")
            return result
        except FileNotFoundError:
            print("Error: Task file not found.")
            logger.error(f"{func.__name__}: Task file missing.")
        except ValueError as e:
            print(f"Invalid input: {e}")
            logger.error(f"{func.__name__}: Invalid input: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
            logger.exception(f"{func.__name__} failed: {e}")
        finally:
            elapsed = round(time.time() - start, 3)
            logger.info(f"{func.__name__} took {elapsed}s")
    return wrapper


# --------------------------------------------------------
# DATACLASS
# --------------------------------------------------------
@dataclass
class Task:
    """Represents a to-do item with title, due date, and creation timestamp."""
    title: str
    due_date: str
    created_at: str = field(default_factory=lambda:
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    @property
    def is_overdue(self):
        """Return True if the task's due date is before today."""
        today = datetime.now().date()
        due_date = datetime.strptime(self.due_date, "%Y-%m-%d").date()
        return due_date < today


# --------------------------------------------------------
# ASYNC TASK MANAGER
# --------------------------------------------------------
class TaskManager:
    """Manage persistence and operations for tasks stored in a JSON file."""
    def __init__(self, storage_file="tasks.json"):
        self._storage_file = storage_file   #Private attribute

    async def _load_tasks(self):
        """Async load tasks with lock and return tasks list from disk; return an empty list if missing."""
        try:
            async with file_lock:
                async with aiofiles.open(self._storage_file, "r") as f:
                    data = await f.read()
                    return json.loads(data) if data else []
        except FileNotFoundError:
            return []

    async def _save_tasks(self, tasks):
        """Async save tasks and Persist current tasks list to disk in pretty-printed JSON."""
        async with file_lock:
            async with aiofiles.open(self._storage_file, "w") as f:
                await f.write(json.dumps(tasks, indent=4))

    # ----------------------------------------------------
    @safe_operation
    async def add_tasks(self, title, due_date):
        """Create a new task and save it to storage."""
        async with file_lock:
            async with aiofiles.open(self._storage_file, "r") as f:
                data = await f.read()
                tasks = json.loads(data) if data else []

            new_task = Task(title, due_date)
            tasks.append(new_task.__dict__)

            async with aiofiles.open(self._storage_file, "w") as f:
                await f.write(json.dumps(tasks, indent=4))

        print(f"Task '{title}' added successfully.")

    # ----------------------------------------------------
    @safe_operation
    async def list_tasks(self):
        """Print all tasks with due date and overdue status."""
        tasks = await self._load_tasks()
        if not tasks:
            print("No tasks found")
            return

        for t in tasks:
            task = Task(**t)
            status = "!! Overdue" if task.is_overdue else "On track"
            print(f"- {task.title} (Due: {task.due_date}) -> {status}")

    # ----------------------------------------------------
    @safe_operation
    async def delete_task(self, title_to_delete):
        """Delete a task by its title and persist the change."""
        async with file_lock:
            async with aiofiles.open(self._storage_file, "r") as f:
                data = await f.read()
                tasks = json.loads(data) if data else []

            updated = [t for t in tasks if t["title"] != title_to_delete]

            if len(updated) == len(tasks):
                print("Task not found")
                return

            async with aiofiles.open(self._storage_file, "w") as f:
                await f.write(json.dumps(updated, indent=4))

        print(f"Task '{title_to_delete}' deleted successfully.")
