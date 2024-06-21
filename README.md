# Task Warrior CLI and Cart API Automation Tests

This project contains automated tests for the Task Warrior CLI application and Cart API using `pytest`.

## Prerequisites

- Python 3.12
- Task Warrior CLI
- pytest

## Setup

#### Create and activate a virtual environment:  

```bash
python3.12 -m venv venv
source venv/bin/activate
```

#### Install dependencies:  
```bash
pip install -r requirements.txt
```

## Run tests

### Task Warrior CLI Tests

```bash
pytest -v tests/taskwarrior
```

### API Tests

```bash
pytest -v tests/api
```

## Linting

To check the code for linting errors, run the following command:

```sh
flake8
```

## Notes and other scenarios

For additional scenarios and notes, please refer to the [notes](notes.md) file.
