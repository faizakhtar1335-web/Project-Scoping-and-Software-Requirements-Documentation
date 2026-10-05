"""
TaskFlow Lite - Simple Task Management System
Week 1 companion implementation for the Software Requirements Document.

Run:
    python task_manager.py

The program demonstrates the core MVP requirements:
- Create tasks
- View tasks
- Mark tasks as completed
- Delete tasks
- Search tasks
- Validate task input
- Save/load tasks from a local JSON file
"""

import json
from pathlib import Path
from datetime import datetime

DATA_FILE = Path("tasks.json")


def load_tasks():
    """Load tasks from the local JSON file."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks):
    """Save the current task list to the local JSON file."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)


def create_task(tasks):
    """Create and store a new task."""
    title = input("Task title: ").strip()
    if not title:
        print("Task title cannot be empty.")
        return

    description = input("Description: ").strip()
    priority = input("Priority (low/medium/high): ").strip().lower()

    if priority not in {"low", "medium", "high"}:
        print("Invalid priority. Using 'medium'.")
        priority = "medium"

    task = {
        "id": max((task["id"] for task in tasks), default=0) + 1,
        "title": title,
        "description": description,
        "priority": priority,
        "completed": False,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }

    tasks.append(task)
    save_tasks(tasks)
    print(f"Task #{task['id']} created successfully.")


def list_tasks(tasks):
    """Display all tasks."""
    if not tasks:
        print("No tasks found.")
        return

    print("\nID | Status | Priority | Title")
    print("-" * 55)

    for task in tasks:
        status = "Done" if task["completed"] else "Pending"
        print(
            f"{task['id']:>2} | "
            f"{status:<7} | "
            f"{task['priority']:<8} | "
            f"{task['title']}"
        )


def complete_task(tasks):
    """Mark a task as completed."""
    try:
        task_id = int(input("Task ID to complete: "))
    except ValueError:
        print("Please enter a valid numeric ID.")
        return

    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(tasks)
            print("Task marked as completed.")
            return

    print("Task not found.")


def delete_task(tasks):
    """Delete a task by ID."""
    try:
        task_id = int(input("Task ID to delete: "))
    except ValueError:
        print("Please enter a valid numeric ID.")
        return

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            print("Task deleted.")
            return

    print("Task not found.")


def search_tasks(tasks):
    """Search task titles and descriptions."""
    keyword = input("Search keyword: ").strip().lower()
    if not keyword:
        print("Search keyword cannot be empty.")
        return

    matches = [
        task for task in tasks
        if keyword in task["title"].lower()
        or keyword in task["description"].lower()
    ]

    if not matches:
        print("No matching tasks found.")
        return

    print(f"\nFound {len(matches)} task(s):")
    for task in matches:
        status = "Done" if task["completed"] else "Pending"
        print(
            f"#{task['id']} - {task['title']} "
            f"[{task['priority']}, {status}]"
        )


def show_menu():
    """Display the main menu."""
    print("\n=== TaskFlow Lite ===")
    print("1. Create task")
    print("2. View tasks")
    print("3. Complete task")
    print("4. Delete task")
    print("5. Search tasks")
    print("6. Exit")


def main():
    """Run the application."""
    tasks = load_tasks()

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_task(tasks)
        elif choice == "2":
            list_tasks(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            search_tasks(tasks)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-6.")


if __name__ == "__main__":
    main()
