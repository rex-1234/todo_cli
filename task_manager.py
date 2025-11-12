"""Task management module: defines `Task` and `TaskManager` for a simple CLI."""

import json
import os
import time
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from dataclasses import dataclass, field
from functools import wraps

# Ensure log directory exists
os.makedirs("logs", exist_ok=True)

# Create rotating file handler
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


def safe_operation(func):
    """Decorator to handle exceptions and log execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            logger.info(f"{func.__name__} executed successfully.")
            return result
        except FileNotFoundError:
            print("Error: Task file not found. Please add a task first.")
            logger.error(f"{func.__name__}: Task file missing.")
        except ValueError as e:
            print(f"Invalid input: {e}")
            logger.error(f"{func.__name__}: Invalid input: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
            logger.exception(f"{func.__name__}: failed with error: {e}")
        finally:
            elapsed = round(time.time() - start_time, 3)
            logger.info(f"{func.__name__} took {elapsed}s")
    return wrapper


@dataclass
class Task:
    """Represents a to-do item with title, due date, and creation timestamp."""
    title: str
    due_date: str
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    @property
    def is_overdue(self):
        """Return True if the task's due date is before today."""
        today = datetime.now().date()
        due = datetime.strptime(self.due_date, "%Y-%m-%d").date()
        return due < today

class TaskManager:
    """Manage persistence and operations for tasks stored in a JSON file."""
    def __init__(self, storage_file="tasks.json"):
        """Initialize the manager with a storage file and load tasks."""
        self._storage_file = storage_file   # Private
        self._tasks = self._load_tasks()

    def _load_tasks(self):
        """Load and return tasks list from disk; return an empty list if missing."""
        try:
            with open(self._storage_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def _save_tasks(self):
        """Persist current tasks list to disk in pretty-printed JSON."""
        with open(self._storage_file, "w", encoding="utf-8") as f:
            json.dump(self._tasks, f, indent=4)

    @safe_operation
    def add_tasks(self, title, due_date):
        """Create a new task and save it to storage."""
        new_task = Task(title, due_date)
        self._tasks.append(new_task.__dict__)
        self._save_tasks()
        print(f"Task '{title}' added successfully.")

    @safe_operation
    def list_tasks(self):
        """Print all tasks with due date and overdue status."""
        if not self._tasks:
            print("No tasks found")
        for t in self._tasks:
            task = Task(**t)
            status = "!! Overdue" if task.is_overdue else "On track"
            print(f"- {t['title']} (Due: {t['due_date']}) -> {status}")

    @safe_operation
    def delete_task(self, title_to_delete):
        """Delete a task by its title and persist the change."""
        if not self._tasks:
            print("No tasks found")
            return
        self._tasks = [task for task in self._tasks if task['title'] != title_to_delete]
        self._save_tasks()
        print(f"Task '{title_to_delete}' deleted successfully.")
