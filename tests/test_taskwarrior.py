import logging
import subprocess
import pytest

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')


def delete_all_tasks():
    """
    Function to delete all tasks.
    """
    subprocess.run(['task', 'rc.confirmation:no', 'rc.bulk:yes', 'rc.report.list.sort:'], capture_output=True, text=True)
    result = subprocess.run(['task', 'delete', 'all'], input='yes\n', capture_output=True, text=True)
    print(result.stdout)


def delete_task_by_id(task_id):
    """
    Function to delete a task by its ID.
    """
    result = subprocess.run(['task', str(task_id), 'delete'], input='yes\n', capture_output=True, text=True)
    print(f"Deleted task {task_id}: {result.stdout}")


@pytest.fixture(autouse=True)
def run_before_tests():
    """
    Fixture to run before each test to delete all tasks.
    """
    delete_all_tasks()


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
    delete_task_by_id(1)  # Remove the created task


def test_taskwarrior_list():
    """
    Test that listing tasks in Taskwarrior includes the recently added task.
    """
    result = subprocess.run(['task', 'add', 'Test task in list'], capture_output=True, text=True)
    assert 'Created task' in result.stdout
    result = subprocess.run(['task', 'list'], capture_output=True, text=True)
    assert 'Test task in list' in result.stdout
    delete_task_by_id(1)  # Remove the created task


def test_taskwarrior_done():
    """
    Test that marking a task as done in Taskwarrior returns a success message.
    """
    result = subprocess.run(['task', 'add', 'Test task finished'], capture_output=True, text=True)
    assert 'Created task' in result.stdout
    result = subprocess.run(['task', '1', 'done'], capture_output=True, text=True)
    assert 'Completed task' in result.stdout
    delete_task_by_id(1)  # Remove the created task


def test_taskwarrior_add_with_priority():
    """
    Test that adding a task with priority returns a success message.
    """
    result = subprocess.run(['task', 'add', 'High priority task', 'priority:H'], capture_output=True, text=True)
    assert 'Created task' in result.stdout
    assert 'High priority task' in subprocess.run(['task', 'list'], capture_output=True, text=True).stdout
    delete_task_by_id(1)  # Remove the created task


def test_taskwarrior_modify():
    """
    Test that modifying a task returns a success message.
    """
    # Add a task to modify
    subprocess.run(['task', 'add', 'Test task modification'], capture_output=True, text=True)
    # Modify the task with ID 1 to have the project 'Home'
    result = subprocess.run(['task', '1', 'modify', 'project:Home'], capture_output=True, text=True)
    assert 'Modified 1 task' in result.stdout

    # Retrieve the task info to verify the modification
    task_info = subprocess.run(['task', '1', 'info'], capture_output=True, text=True).stdout

    # Split the output into lines in order to locate the project line
    lines = task_info.split('\n')

    # Find the line that contains 'Project'
    project_line = next(line for line in lines if 'Project' in line)
    logging.debug("Project line: %s", project_line)

    # Assert that 'Home' is in the trimmed parts of the project line
    assert 'Home' in project_line.split()
    delete_task_by_id(1)  # Remove the created task


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
    # Add a task to start
    subprocess.run(['task', 'add', 'Test task start'], capture_output=True, text=True)
    result = subprocess.run(['task', '1', 'start'], capture_output=True, text=True)
    assert 'Started 1 task' in result.stdout
    delete_task_by_id(1)  # Remove the created task


def test_taskwarrior_stop():
    """
    Test that stopping a task returns a success message.
    """
    # Add a task to stop
    subprocess.run(['task', 'add', 'Test task stop'], capture_output=True, text=True)

    # Start the task
    subprocess.run(['task', '1', 'start'], capture_output=True, text=True)

    # Stop the task
    result = subprocess.run(['task', '1', 'stop'], capture_output=True, text=True)
    assert 'Stopped 1 task' in result.stdout

    delete_task_by_id(1)  # Remove the created task


def test_taskwarrior_annotate():
    """
    Test that adding an annotation to a task returns a success message.
    """
    # Add a task to annotate
    subprocess.run(['task', 'add', 'Test task note'], capture_output=True, text=True)
    result = subprocess.run(['task', '1', 'annotate', 'This is a note'], capture_output=True, text=True)
    assert 'Annotated 1 task' in result.stdout
    delete_task_by_id(1)  # Remove the created task
