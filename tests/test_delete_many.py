import pytest
import asyncio

@pytest.mark.asyncio
async def test_delete_multiple_tasks(manager):
    """Test deleting multiple tasks."""
    await manager.add_tasks("Task A", "2025-12-31")
    await manager.add_tasks("Task B", "2025-11-30")
    await manager.add_tasks("Task C", "2025-12-15")

    titles_to_delete = ["Task A", "Task C"]
    async with asyncio.TaskGroup() as tg:
        for title in titles_to_delete:
            tg.create_task(manager.delete_task(title))

    tasks = await manager._load_tasks()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Task B"