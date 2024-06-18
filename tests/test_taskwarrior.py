from task_operations import *

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')


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
    result = add_task('Test task')
    assert 'Created task' in result.stdout
    delete_task_by_id(1)  # Remove the created task


def test_taskwarrior_list():
    """
    Test that listing tasks in Taskwarrior includes the recently added task.
    """
    result = add_task('Test task in list')
    assert 'Created task' in result.stdout
    result = list_tasks()
    assert 'Test task in list' in result.stdout
    delete_task_by_id(1)  # Remove the created task


def test_taskwarrior_done():
    """
    Test that marking a task as done in Taskwarrior returns a success message.
    """
    result = add_task('Test task finished')
    assert 'Created task' in result.stdout
    result = subprocess.run(['task', '1', 'done'], capture_output=True, text=True)
    assert 'Completed task' in result.stdout
    delete_task_by_id(1)  # Remove the created task


def test_taskwarrior_add_with_priority():
    """
    Test that adding a task with priority returns a success message.
    """
    result = add_task('High priority task', 'priority:H')
    assert 'Created task' in result.stdout
    assert 'High priority task' in list_tasks().stdout
    delete_task_by_id(1)  # Remove the created task


def test_taskwarrior_modify():
    """
    Test that modifying a task returns a success message.
    """
    add_task('Test task modification')
    result = modify_task(1, 'project:Home')
    assert 'Modified 1 task' in result.stdout

    task_info = get_task_info(1).stdout
    lines = task_info.split('\n')
    project_line = next(line for line in lines if 'Project' in line)
    logging.debug("Project line: %s", project_line)
    assert 'Home' in project_line.split()
    delete_task_by_id(1)  # Remove the created task


def test_taskwarrior_start():
    """
    Test that starting a task returns a success message.
    """
    add_task('Test task start')
    result = start_task(1)
    assert 'Started 1 task' in result.stdout
    delete_task_by_id(1)  # Remove the created task


def test_taskwarrior_stop():
    """
    Test that stopping a task returns a success message.
    """
    add_task('Test task stop')
    start_task(1)
    result = stop_task(1)
    assert 'Stopped 1 task' in result.stdout
    delete_task_by_id(1)  # Remove the created task


def test_taskwarrior_annotate():
    """
    Test that adding an annotation to a task returns a success message.
    """
    add_task('Test task note')
    result = annotate_task(1, 'This is a note')
    assert 'Annotated 1 task' in result.stdout
    delete_task_by_id(1)  # Remove the created task
