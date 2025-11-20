import pytest

@pytest.mark.asyncio
async def test_add_single_task(manager):
    """Test adding a single task."""
    await manager.add_tasks("Test A", "2025-12-31")
    tasks = await manager._load_tasks()

    assert len(tasks) == 1
    assert tasks[0]["title"] == "Test A"
    assert tasks[0]["due_date"] == "2025-12-31"
