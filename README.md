# Python Todo

A lightweight command-line todo application. It uses only the Python standard library and stores tasks in a local `todos.json` file.

## Requirements

- Python 3.10 or newer
- No third-party packages

## Quick start

Clone the repository and open its directory:

```bash
git clone https://github.com/nauman34/todo.git
cd todo
```

Add a task:

```bash
python todo.py add "Prepare project report"
```

List pending tasks:

```bash
python todo.py list
```

List all tasks, including completed tasks:

```bash
python todo.py list --all
```

Mark a task complete (replace `1` with its ID):

```bash
python todo.py done 1
```

Edit or delete a task:

```bash
python todo.py edit 1 "Prepare final project report"
python todo.py delete 1
```

On Windows, use `py` instead of `python` if that is your Python launcher:

```powershell
py todo.py add "My first task"
py todo.py list --all
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Data and privacy

Tasks are saved in `todos.json` beside the application. The file is created automatically and is excluded from Git so your personal tasks are not committed.
