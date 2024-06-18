import pytest
from task_operations import delete_all_tasks


@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    """
    Fixture to run before and after each test to delete all tasks.
    """
    delete_all_tasks()
    yield
    delete_all_tasks()
