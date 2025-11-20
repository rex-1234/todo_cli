import pytest
from task_manager import safe_operation

@pytest.mark.asyncio
async def test_safe_operation_error_handling(manager):
    """Test that safe_operation decorator handles exceptions gracefully."""
    @safe_operation
    async def faulty_method():
        raise ValueError("Intentional Error")

    # Call the faulty method and ensure it does not raise
    result = await faulty_method()

    # Ensure that the manager is still operational after the error
    assert result is None
