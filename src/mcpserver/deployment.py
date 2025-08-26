from mcp.server.fastmcp import FastMCP
from mcpserver.utils import read_tasks, write_task, Task

mcp = FastMCP("todo")

filename = "tasks.json"

@mcp.tool()
def add_task(task: Task) -> str:
    """
    Adds a task to the to-do list.

    Args:
        task (Task): The task to add.

    Returns:
        str: Confirmation message.
    """
    # In a real implementation, this function would save the task to a database or file.
    write_task(filename, task)
    return f"Task '{task.title}' added to your to-do list."

@mcp.tool()
def list_tasks() -> str:
    """
    Lists all tasks in the to-do list.

    Returns:
        str: A list of tasks.
    """
    tasks = read_tasks(filename)
    if not tasks:
        return "No tasks found."
    lines = []
    for task in tasks:
        status = "✅ Done" if task.completed else "📝 Pending"
        lines.append(f"[{task.id}] {task.title} - {status}\n   {task.description}")

    return "Tasks found:\n" + "\n".join(lines)
