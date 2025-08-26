import json
from pathlib import Path
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field
from datetime import datetime

class Task(BaseModel):
    id: int = Field(default_factory=int)
    title: str
    description: str
    completed: bool = False
    created_at: datetime = datetime.now()
    completed_at: datetime | None = None


def read_tasks(file_path: str) -> List[Task]:
    """
    Reads tasks from a JSON file and returns a list of Task objects.
    If file does not exist or is invalid, returns an empty list.
    """
    path = Path(file_path)
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                return []
            return [Task(**item) for item in data]
    except (json.JSONDecodeError, OSError, TypeError, ValueError):
        return []

def write_task(file_path: str, task: Task) -> bool:
    """
    Appends a Task object to the JSON file.
    If file doesn't exist, creates it with a list containing the task.
    """
    path = Path(file_path)

    # Read existing tasks (or start fresh)
    tasks = read_tasks(file_path)

    if not isinstance(tasks, list):
        tasks = []

    # Convert task to dict, making datetime JSON-safe
    def default_serializer(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")

    task_dict = task.model_dump()

    tasks.append(task_dict)

    try:
        with path.open("w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=4, ensure_ascii=False, default=default_serializer)
        return True
    except OSError:
        return False
    
def complete_task(task_id: int) -> str:
    """
    Marks a task as completed.
    """
    tasks = read_tasks("tasks.json")
    if not tasks:
        return f"No tasks found. Cannot complete task {task_id}."

    for task in tasks:
        if task.id == task_id:
            if task.completed:
                return f"Task {task_id} ('{task.title}') is already completed."

            task.completed = True
            task.completed_at = datetime.now()
            save_tasks("tasks.json", tasks)
            return f"Task {task_id} ('{task.title}') marked as completed ✅."

    return f"Task with ID {task_id} not found."

def delete_task(task_id: int) -> str:
    """
    Deletes a task from the to-do list.
    Args:
        task_id (int): The ID of the task to delete.

    Returns:
        str: Confirmation message.
    """
    tasks = read_tasks("tasks.json")
    if not tasks:
        return f"No tasks found. Cannot delete task {task_id}."

    # Find the task
    for task in tasks:
        if task.id == task_id:

            tasks.remove(task)
            save_tasks("tasks.json", tasks)
            return f"Task {task_id} ('{task.title}') deleted from your to-do list 🗑️."

    return f"Task with ID {task_id} not found."

def save_tasks(file_path: str, tasks: list[Task]) -> bool:
    """
    Saves the entire list of Task objects to the JSON file.
    Overwrites the file.
    """
    path = Path(file_path)

    def default_serializer(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")

    try:
        # Use model_dump() to avoid recursion
        data = [t.model_dump() for t in tasks]
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False, default=default_serializer)
        return True
    except OSError:
        return False