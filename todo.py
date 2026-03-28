#!/usr/bin/env python3
"""
todo.py - A simple command-line todo manager.

Usage:
    python todo.py add "Buy groceries"
    python todo.py list
    python todo.py done 1
    python todo.py delete 1
"""

import argparse
import json
import os
import sys
from datetime import datetime

TASKS_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def add_task(title):
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "done": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added task #{task['id']}: {title}")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks yet. Add one with: python todo.py add \"your task\"")
        return
    print(f"\n{'#':<4} {'Status':<8} {'Created':<18} Title")
    print("-" * 60)
    for task in tasks:
        status = "[x]" if task["done"] else "[ ]"
        print(f"{task['id']:<4} {status:<8} {task['created_at']:<18} {task['title']}")
    print()


def complete_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            if task["done"]:
                print(f"Task #{task_id} is already marked as done.")
            else:
                task["done"] = True
                save_tasks(tasks)
                print(f"Marked task #{task_id} as done: {task['title']}")
            return
    print(f"Task #{task_id} not found.")
    sys.exit(1)


def delete_task(task_id):
    tasks = load_tasks()
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            removed = tasks.pop(i)
            save_tasks(tasks)
            print(f"Deleted task #{task_id}: {removed['title']}")
            return
    print(f"Task #{task_id} not found.")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="A simple command-line todo manager.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python todo.py add "Write unit tests"
  python todo.py list
  python todo.py done 1
  python todo.py delete 2
        """,
    )
    subparsers = parser.add_subparsers(dest="command", metavar="command")
    subparsers.required = True

    # add
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="The task description")

    # list
    subparsers.add_parser("list", help="List all tasks")

    # done
    done_parser = subparsers.add_parser("done", help="Mark a task as complete")
    done_parser.add_argument("id", type=int, help="Task ID to mark as done")

    # delete
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID to delete")

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.title)
    elif args.command == "list":
        list_tasks()
    elif args.command == "done":
        complete_task(args.id)
    elif args.command == "delete":
        delete_task(args.id)


if __name__ == "__main__":
    main()
