import subprocess


def test_taskwarrior_version():
    # Test that Task warrior's version command returns the expected version format
    result = subprocess.run(['task', '--version'], capture_output=True, text=True)
    assert result.stdout.startswith('3.')


def test_taskwarrior_add():
    # Test that adding a task to Taskwarrior returns a success message
    result = subprocess.run(['task', 'add', 'Test task'], capture_output=True, text=True)
    assert 'Created task' in result.stdout


def test_taskwarrior_list():
    # Test that listing tasks in Taskwarrior includes the recently added task
    result = subprocess.run(['task', 'list'], capture_output=True, text=True)
    assert 'Test task' in result.stdout


def test_taskwarrior_done():
    # Test that marking a task as done in Taskwarrior returns a success message
    result = subprocess.run(['task', '1', 'done'], capture_output=True, text=True)
    assert 'Completed task' in result.stdout
