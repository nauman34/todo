"""Flask web interface for the todo application."""
import os
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_wtf.csrf import CSRFProtect
from todo import add_task, find_task, load_tasks, save_tasks

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev-only-change-this-secret")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024
CSRFProtect(app)


@app.get("/")
def index():
    tasks = load_tasks()
    status = request.args.get("status", "all")
    if status == "pending":
        tasks = [task for task in tasks if not task.get("completed")]
    elif status == "completed":
        tasks = [task for task in tasks if task.get("completed")]
    elif status != "all":
        status = "all"
    total = load_tasks()
    return render_template(
        "index.html",
        tasks=tasks,
        status=status,
        total=len(total),
        completed=sum(bool(task.get("completed")) for task in total),
        pending=sum(not task.get("completed") for task in total),
    )


@app.post("/add")
def add():
    title = request.form.get("title", "").strip()
    try:
        if len(title) > 200:
            raise ValueError("Task title must be 200 characters or fewer.")
        tasks = load_tasks()
        task = add_task(tasks, title)
        save_tasks(tasks)
        flash(f'Task "{task["title"]}" added.', "success")
    except (ValueError, RuntimeError, OSError) as exc:
        flash(str(exc), "danger")
    return redirect(url_for("index"))


@app.post("/<int:task_id>/toggle")
def toggle(task_id):
    try:
        tasks = load_tasks()
        task = find_task(tasks, task_id)
        task["completed"] = not task.get("completed", False)
        save_tasks(tasks)
        flash("Task status updated.", "success")
    except (ValueError, RuntimeError, OSError) as exc:
        flash(str(exc), "danger")
    return redirect(url_for("index"))


@app.post("/<int:task_id>/edit")
def edit(task_id):
    title = request.form.get("title", "").strip()
    try:
        if not title:
            raise ValueError("Task title cannot be empty.")
        if len(title) > 200:
            raise ValueError("Task title must be 200 characters or fewer.")
        tasks = load_tasks()
        task = find_task(tasks, task_id)
        task["title"] = title
        save_tasks(tasks)
        flash("Task updated.", "success")
    except (ValueError, RuntimeError, OSError) as exc:
        flash(str(exc), "danger")
    return redirect(url_for("index"))


@app.post("/<int:task_id>/delete")
def delete(task_id):
    try:
        tasks = load_tasks()
        task = find_task(tasks, task_id)
        tasks.remove(task)
        save_tasks(tasks)
        flash("Task deleted.", "success")
    except (ValueError, RuntimeError, OSError) as exc:
        flash(str(exc), "danger")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")), debug=False)
