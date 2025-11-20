import pytest
import asyncio

@pytest.mark.asyncio
async def test_add_multiple_tasks(manager):
    """Test adding multiple tasks."""
    tasks_to_add = [("Task A", "2025-12-31"), ("Task B", "2025-11-30"), ("Task C", "2025-12-15")]

    async with asyncio.TaskGroup() as tg:
        for title, due_date in tasks_to_add:
            tg.create_task(manager.add_tasks(title, due_date))

    tasks = await manager._load_tasks()
    titles = {task["title"] for task in tasks}

    assert len(tasks) == 3
    assert titles == {"Task A", "Task B", "Task C"}