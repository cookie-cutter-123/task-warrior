import logging
import subprocess
import pytest

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')


@pytest.fixture(scope='module', autouse=True)
def cleanup_tasks():
    """
    Fixture to clean up all tasks after the tests are run.
    This runs once per module and deletes all tasks by running 'task delete all'.
    """
    yield
    # Delete all tasks after tests
    subprocess.run(['task', 'rc.confirmation:no', 'rc.bulk:yes', 'rc.report.list.sort:'], capture_output=True, text=True)
    result = subprocess.run(['task', 'delete', 'all'], input='yes\n', capture_output=True, text=True)
    print(result.stdout)


def test_taskwarrior_version():
    """
    Test that Task warrior's version command returns the expected version format.
    """
    result = subprocess.run(['task', '--version'], capture_output=True, text=True)
    assert result.stdout.startswith('3.')


def test_taskwarrior_add():
    """
    Test that adding a task to Taskwarrior returns a success message.
    """
    result = subprocess.run(['task', 'add', 'Test task'], capture_output=True, text=True)
    assert 'Created task' in result.stdout


def test_taskwarrior_list():
    """
    Test that listing tasks in Taskwarrior includes the recently added task.
    """
    result = subprocess.run(['task', 'list'], capture_output=True, text=True)
    assert 'Test task' in result.stdout


def test_taskwarrior_done():
    """
    Test that marking a task as done in Taskwarrior returns a success message.
    """
    result = subprocess.run(['task', '1', 'done'], capture_output=True, text=True)
    assert 'Completed task' in result.stdout


def test_taskwarrior_add_with_priority():
    """
    Test that adding a task with priority returns a success message.
    """
    result = subprocess.run(['task', 'add', 'High priority task', 'priority:H'], capture_output=True, text=True)
    assert 'Created task' in result.stdout
    assert 'High priority task' in subprocess.run(['task', 'list'], capture_output=True, text=True).stdout


def test_taskwarrior_modify():
    """
    Test that modifying a task returns a success message.
    """
    # Modify the task with ID 2 to have the project 'Home'
    result = subprocess.run(['task', '2', 'modify', 'project:Home'], capture_output=True, text=True)
    assert 'Modified 1 task' in result.stdout

    # Retrieve the task info to verify the modification
    task_info = subprocess.run(['task', '2', 'info'], capture_output=True, text=True).stdout

    # Split the output into lines in order to locate the project line
    lines = task_info.split('\n')

    # Find the line that contains 'Project'
    project_line = next(line for line in lines if 'Project' in line)
    logging.debug("Project line: %s", project_line)

    # Assert that 'Home' is in the trimmed parts of the project line
    assert 'Home' in project_line.split()


def test_taskwarrior_delete():
    """
    Test that deleting a task returns a success message.
    """
    # List tasks before deletion
    task_list_before = subprocess.run(['task', 'list'], capture_output=True, text=True).stdout
    logging.debug("Task list before deletion: " + task_list_before)

    # Delete the task with ID 2
    result = subprocess.run(['task', '2', 'delete'], input='yes\n', capture_output=True, text=True)
    assert 'Deleted 1 task' in result.stdout

    # List tasks after deletion
    task_list_after = subprocess.run(['task', 'list'], capture_output=True, text=True).stdout
    logging.debug("Task list after deletion: " + task_list_after)
    # TODO assert that the test task is no longer in the list


def test_taskwarrior_start():
    """
    Test that starting a task returns a success message.
    """
    result = subprocess.run(['task', '3', 'start'], capture_output=True, text=True)
    assert 'Started 1 task' in result.stdout


def test_taskwarrior_stop():
    """
    Test that stopping a task returns a success message.
    """
    result = subprocess.run(['task', '3', 'stop'], capture_output=True, text=True)
    assert 'Stopped 1 task' in result.stdout


def test_taskwarrior_annotate():
    """
    Test that adding an annotation to a task returns a success message.
    """
    result = subprocess.run(['task', '3', 'annotate', 'This is a note'], capture_output=True, text=True)
    assert 'Annotated 1 task' in result.stdout
