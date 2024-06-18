import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')


def delete_all_tasks():
    """
    Function to delete all tasks.
    This function repeatedly fetches the list of tasks
    and deletes them until no tasks remain.
    """
    while True:
        # Fetch the list of tasks
        result = subprocess.run(['task', 'list'], capture_output=True, text=True)

        # Extract task IDs from the output
        task_ids = [line.split()[0] for line in result.stdout.split(
            '\n') if line.strip() and line.split()[0].isdigit()]

        # Break the loop if there are no task IDs
        if not task_ids:
            break

        # Delete each task by ID
        for task_id in task_ids:
            subprocess.run(['task', task_id, 'delete'], input='yes\n',
                           capture_output=True, text=True)

        # Fetch the list of tasks again to check if any remain
        result = subprocess.run(['task', 'list'], capture_output=True, text=True)

        # Break the loop if no tasks remain
        if "No matches" in result.stdout:
            break


def delete_task_by_id(task_id):
    """
    Function to delete a task by its ID.
    """
    result = subprocess.run(['task', str(task_id), 'delete'],
                            input='yes\n', capture_output=True, text=True)
    logging.debug(f"Deleted task {task_id}: {result.stdout}")
    assert 'Deleted 1 task' in result.stdout


def add_task(description, *args):
    """
    Function to add a task with a description and optional arguments.
    """
    return subprocess.run(['task', 'add', description, *args],
                          capture_output=True, text=True)


def modify_task(task_id, *args):
    """
    Function to modify a task by its ID with the provided arguments.
    """
    return subprocess.run(['task', str(task_id), 'modify', *args],
                          capture_output=True, text=True)


def start_task(task_id):
    """
    Function to start a task by its ID.
    """
    return subprocess.run(['task', str(task_id), 'start'],
                          capture_output=True, text=True)


def stop_task(task_id):
    """
    Function to stop a task by its ID.
    """
    return subprocess.run(['task', str(task_id), 'stop'],
                          capture_output=True, text=True)


def annotate_task(task_id, note):
    """
    Function to add an annotation to a task by its ID.
    """
    return subprocess.run(['task', str(task_id), 'annotate', note],
                          capture_output=True, text=True)


def get_task_info(task_id):
    """
    Function to get information about a task by its ID.
    """
    return subprocess.run(['task', str(task_id), 'info'],
                          capture_output=True, text=True)


def list_tasks():
    """
    Function to list all tasks.
    """
    return subprocess.run(['task', 'list'], capture_output=True, text=True)
