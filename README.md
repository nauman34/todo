# Python Todo

A lightweight todo manager with both a command-line interface and a responsive Flask web interface. Tasks are stored locally in todos.json.

## Requirements

- Python 3.10 or newer
- Flask and Flask-WTF (install from requirements.txt)

## Run the web application

Clone the repository and open its directory:

```bash
git clone https://github.com/nauman34/todo.git
cd todo
```

Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate
```

Install dependencies and start Flask:

```bash
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser.

For a persistent secret key, set FLASK_SECRET_KEY before starting the app. On Windows PowerShell:

```powershell
$env:FLASK_SECRET_KEY = "replace-with-a-long-random-secret"
python app.py
```

The development server binds to localhost only. For production, use a production WSGI server (such as Waitress or Gunicorn), configure a strong secret key, and deploy behind HTTPS.

## Command-line interface

The original CLI remains available:

```bash
python todo.py add "Prepare project report"
python todo.py list
python todo.py list --all
python todo.py done 1
python todo.py edit 1 "Prepare final project report"
python todo.py delete 1
```

On Windows, use py instead of python if needed.

## Features

- Add, edit, complete, delete, and filter tasks
- Dashboard counts for total, pending, and completed tasks
- Responsive Bootstrap 5 interface
- CSRF protection on form submissions
- JSON file persistence shared by the CLI and web app

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Data and privacy

Tasks are saved in todos.json beside the application. The file is created automatically and excluded from Git. Do not expose the Flask development server directly to the public internet.
