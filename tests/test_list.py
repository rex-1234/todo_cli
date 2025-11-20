import pytest
from io import StringIO
from unittest.mock import patch

@pytest.mark.asyncio
async def test_list_tasks(manager):
    await manager.add_tasks("Test A", "2025-12-31")

    with patch("sys.stdout", new=StringIO()) as fake_out:
        await manager.list_tasks()
        output = fake_out.getvalue().strip()

    assert "Test A" in output
    assert "Due: 2025-12-31" in output
