#!/usr/bin/env python3
"""A small command-line todo manager with local JSON persistence."""
from __future__ import annotations

import argparse
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DATA_FILE = Path(__file__).with_name("todos.json")


def load_tasks(path: Path = DATA_FILE) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise RuntimeError(f"Cannot read task data from {path}: {exc}") from exc
    if not isinstance(data, list):
        raise RuntimeError(f"Invalid task data in {path}: expected a JSON list")
    return data


def save_tasks(tasks: list[dict[str, Any]], path: Path = DATA_FILE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(tasks, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def next_id(tasks: list[dict[str, Any]]) -> int:
    return max((int(task.get("id", 0)) for task in tasks), default=0) + 1


def add_task(tasks: list[dict[str, Any]], title: str) -> dict[str, Any]:
    title = title.strip()
    if not title:
        raise ValueError("Task title cannot be empty.")
    task = {
        "id": next_id(tasks),
        "title": title,
        "completed": False,
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    tasks.append(task)
    return task


def find_task(tasks: list[dict[str, Any]], task_id: int) -> dict[str, Any]:
    for task in tasks:
        if task.get("id") == task_id:
            return task
    raise ValueError(f"No task found with ID {task_id}.")


def print_tasks(tasks: list[dict[str, Any]], show_all: bool = False) -> None:
    visible = tasks if show_all else [task for task in tasks if not task.get("completed")]
    if not visible:
        print("No tasks to show.")
        return
    print(f"{'ID':<5} {'Status':<12} Task")
    print("-" * 52)
    for task in visible:
        status = "Done" if task.get("completed") else "Pending"
        print(f"{task['id']:<5} {status:<12} {task['title']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="A simple command-line todo application.")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add", help="Add a new task")
    add.add_argument("title", help="Task description")
    listing = sub.add_parser("list", help="List tasks")
    listing.add_argument("--all", action="store_true", help="Include completed tasks")
    done = sub.add_parser("done", help="Mark a task as completed")
    done.add_argument("id", type=int, help="Task ID")
    delete = sub.add_parser("delete", help="Delete a task")
    delete.add_argument("id", type=int, help="Task ID")
    edit = sub.add_parser("edit", help="Change a task title")
    edit.add_argument("id", type=int, help="Task ID")
    edit.add_argument("title", help="New task description")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        tasks = load_tasks()
        if args.command == "add":
            task = add_task(tasks, args.title)
            save_tasks(tasks)
            print(f"Added task #{task['id']}: {task['title']}")
        elif args.command == "list":
            print_tasks(tasks, args.all)
        elif args.command == "done":
            task = find_task(tasks, args.id)
            task["completed"] = True
            save_tasks(tasks)
            print(f"Completed task #{task['id']}: {task['title']}")
        elif args.command == "delete":
            task = find_task(tasks, args.id)
            tasks.remove(task)
            save_tasks(tasks)
            print(f"Deleted task #{args.id}.")
        elif args.command == "edit":
            task = find_task(tasks, args.id)
            title = args.title.strip()
            if not title:
                raise ValueError("Task title cannot be empty.")
            task["title"] = title
            save_tasks(tasks)
            print(f"Updated task #{args.id}.")
        return 0
    except (RuntimeError, ValueError, OSError) as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
