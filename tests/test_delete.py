import pytest

@pytest.mark.asyncio
async def test_delete_single_task(manager):
    """Test deleting a single task."""
    await manager.add_tasks("Test A", "2025-12-31")
    await manager.add_tasks("Test B", "2025-11-30")

    await manager.delete_task("Test A")
    tasks = await manager._load_tasks()

    assert len(tasks) == 1
    assert tasks[0]["title"] == "Test B"
