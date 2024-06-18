# Task Warrior CLI Automation Tests

This project contains automated tests for the Task Warrior CLI application using `pytest`.

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

```bash
pytest -v tests
```

## Linting

To check the code for linting errors, run the following command:

```sh
flake8
```
