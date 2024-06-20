import logging
from tests.taskwarrior.task_operations import (
    add_task,
    delete_task_by_id,
    list_tasks,
    modify_task,
    get_task_info,
    start_task,
    stop_task,
    annotate_task,
    find_line_containing_keyword,
    mark_task_done,
    check_taskwarrior_version
)
import pytest

# Create a logger object named after the current module
logger = logging.getLogger(__name__)


@pytest.mark.skip(
    reason="Skipping this test because default APT version"
           "is different and tests are failing on server."
           "The newer version can be downloaded from here if needed: "
           "https://github.com/GothenburgBitFactory/taskwarrior/releases")
def test_taskwarrior_version():
    """
    Test that Task warrior's version command returns the expected version format.
    """
    result = check_taskwarrior_version()
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
    result = mark_task_done(1)
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
    project_line = find_line_containing_keyword(task_info, 'Project')
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


def test_taskwarrior_project():
    """
    Test that adding a task with a project returns a success message.
    """
    result = add_task('Project task', 'project:Home')
    assert 'Created task' in result.stdout
    assert 'Home' in get_task_info(1).stdout
    delete_task_by_id(1)  # Remove the created task


def test_taskwarrior_due():
    """
    Test that adding a task with a due date returns a success message.
    """
    result = add_task('Task with due date', 'due:tomorrow')
    assert 'Created task' in result.stdout
    assert 'due' in get_task_info(1).stdout
    delete_task_by_id(1)  # Remove the created task


def test_taskwarrior_tag():
    """
    Test that adding a task with a tag returns a success message.
    """
    result = add_task('Tagged task', '+urgent')
    assert 'Created task' in result.stdout

    task_info = get_task_info(1).stdout
    tag_line = find_line_containing_keyword(task_info, 'Tags')
    logging.debug("Tag line: %s", tag_line)

    # Assert that the tag 'urgent' is in the tags line
    assert 'urgent' in tag_line.split()
    delete_task_by_id(1)  # Remove the created task
