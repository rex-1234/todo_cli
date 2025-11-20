import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest_asyncio
import tempfile
import os
from task_manager import TaskManager

@pytest_asyncio.fixture
async def tmp_task_file():
    """Isolated temporary storage file for each test."""
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.close()
    yield temp.name
    os.remove(temp.name)

@pytest_asyncio.fixture
async def manager(tmp_task_file):
    """TaskManager instance using isolated temp file."""
    return TaskManager(storage_file=tmp_task_file)
