import json
from utils import clear_screen, style_text, GREEN, RED, UNDERLINE


def load_tasks():
    """
    Loads tasks from the 'tasks.json' file.

    Returns:
        dict: A dictionary where the keys are dates (in "YYYY-MM-DD" format)
              and the values are lists of tasks for those dates.
    """
    with open("tasks.json", "r") as f:
        return json.load(f)


def save_tasks(tasks):
    """
    Saves the given tasks to the 'tasks.json' file.

    Args:
        tasks (dict): A dictionary where the keys are dates (in "YYYY-MM-DD" format)
                      and the values are lists of tasks for those dates.
    """
    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=4)


def get_tasks_for_day(year, month, day):
    """
    Retrieves the tasks for a specific day.

    Args:
        year (int): The year of the day.
        month (int): The month of the day.
        day (int): The day of the month.

    Returns:
        list: A list of tasks for the specified day.
    """
    tasks = load_tasks()
    date_str = f"{year}-{month:02d}-{day:02d}"
    return tasks.get(date_str, [])


def add_task(year, month, day, task_name):
    """
    Adds a task to the specified day.

    Args:
        year (int): The year of the day.
        month (int): The month of the day.
        day (int): The day of the month.
        task_name (str): The name of the task to add.
    """
    tasks = load_tasks()
    date_str = f"{year}-{month:02d}-{day:02d}"

    if date_str not in tasks:
        tasks[date_str] = []

    tasks[date_str].append({"task": task_name, "status": "pending"})
    save_tasks(tasks)


def toggle_status(year, month, day, task_index):
    """
    Toggles the status of a task between 'pending' and 'completed'.

    Args:
        year (int): The year of the day.
        month (int): The month of the day.
        day (int): The day of the month.
        task_index (int): The index of the task to toggle.
    """
    tasks = get_tasks_for_day(year, month, day)

    if 0 <= task_index < len(tasks):
        task = tasks[task_index]
        task["status"] = "completed" if task["status"] == "pending" else "pending"

        date_str = f"{year}-{month:02d}-{day:02d}"
        all_tasks = load_tasks()
        all_tasks[date_str] = tasks

        save_tasks(all_tasks)


def delete_task(year, month, day, task_index):
    """
    Deletes a task from the specified day.

    Args:
        year (int): The year of the day.
        month (int): The month of the day.
        day (int): The day of the month.
        task_index (int): The index of the task to delete.
    """
    tasks = load_tasks()
    date_str = f"{year}-{month:02d}-{day:02d}"

    if date_str in tasks and 0 <= task_index < len(tasks[date_str]):
        del tasks[date_str][task_index]
        if not tasks[date_str]:
            del tasks[date_str]
        save_tasks(tasks)


def display_task_for_day(year, month, day, mode="main"):
    """
    Displays the tasks for a specific day, and provides options to create, delete, or toggle tasks.

    Args:
        year (int): The year of the day.
        month (int): The month of the day.
        day (int): The day of the month.
        mode (str): The mode for displaying tasks. "main" shows all options,
        "delete" or "toggle" restricts to delete or toggle actions.
    """
    tasks = get_tasks_for_day(year, month, day)
    print(f"\n {style_text(f'{year}-{month:02d}-{day:02d}', UNDERLINE)}:\n")

    if tasks:
        for index, task in enumerate(tasks, start=1):
            status_color = GREEN if task["status"] == "completed" else RED
            status_text = f"[{style_text(task['status'].capitalize(), status_color)}]".ljust(22)
            print(f" {index}. {status_text} {task['task']}")

        if mode == "main":
            print("\n\n [C] Create Task  [D] Delete Task [T] Toggle Status [B] Go Back [Q] Quit\n")
        else:
            action_text = "Delete Task" if mode == "delete" else "Toggle Status"
            print(f"\n\n [{len(tasks) if len(tasks) == 1 else '1-' + str(len(tasks))}] {action_text}  [B] Go Back"
                  f"  [Q] Quit\n")
    else:
        print(" No tasks for this day.")
        print("\n\n [C] Create Task  [B] Go Back  [Q] Quit\n")


def handle_task_management(year, month, day):
    """
    Handles the task management interface, allowing the user to create, delete, or toggle task statuses.

    Args:
        year (int): The year of the day.
        month (int): The month of the day.
        day (int): The day of the month.
    """
    def create_task():
        clear_screen()
        task_name = input(" Enter task: ").strip()
        if task_name:
            add_task(year, month, day, task_name)

    def modify_task(mode):
        tasks = get_tasks_for_day(year, month, day)
        if not tasks:
            return
        while True:
            clear_screen()
            display_task_for_day(year, month, day, mode=mode)
            task_index = input(" ").strip().lower()
            if task_index == "b":
                break
            elif task_index == "q":
                exit()
            elif task_index.isdigit():
                idx = int(task_index) - 1
                if 0 <= idx < len(tasks):
                    if mode == "delete":
                        delete_task(year, month, day, idx)
                        tasks = get_tasks_for_day(year, month, day)
                        if not tasks:
                            break
                    else:
                        toggle_status(year, month, day, idx)

    actions = {
        "c": create_task,
        "d": lambda: modify_task("delete"),
        "t": lambda: modify_task("toggle"),
        "q": exit,
    }

    while True:
        clear_screen()
        display_task_for_day(year, month, day)
        action = input(" ").strip().lower()
        if action == "b":
            break
        actions.get(action, lambda: None)()
