import json
from utils import clear_screen, color_text, GREEN, RED, UNDERLINE


def load_tasks():
    with open("tasks.json", "r") as f:
        return json.load(f)


def save_tasks(tasks):
    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=4)


def get_tasks_for_day(year, month, day):
    tasks = load_tasks()
    date_str = f"{year}-{month:02d}-{day:02d}"
    return tasks.get(date_str, [])


def add_task(year, month, day, task_name):
    tasks = load_tasks()
    date_str = f"{year}-{month:02d}-{day:02d}"

    if date_str not in tasks:
        tasks[date_str] = []

    tasks[date_str].append({"task": task_name, "status": "pending"})
    save_tasks(tasks)


def toggle_status(year, month, day, task_index):
    tasks = get_tasks_for_day(year, month, day)

    if 0 <= task_index < len(tasks):
        task = tasks[task_index]
        task["status"] = "completed" if task["status"] == "pending" else "pending"

        date_str = f"{year}-{month:02d}-{day:02d}"
        all_tasks = load_tasks()
        all_tasks[date_str] = tasks

        save_tasks(all_tasks)


def delete_task(year, month, day, task_index):
    tasks = load_tasks()
    date_str = f"{year}-{month:02d}-{day:02d}"

    if date_str in tasks and 0 <= task_index < len(tasks[date_str]):
        del tasks[date_str][task_index]
        if not tasks[date_str]:
            del tasks[date_str]
        save_tasks(tasks)


def display_task_for_day(year, month, day, mode="main"):
    tasks = get_tasks_for_day(year, month, day)
    print(f"\n {color_text(f'{year}-{month:02d}-{day:02d}', UNDERLINE)}:\n")

    if tasks:
        for index, task in enumerate(tasks, start=1):
            status_color = GREEN if task["status"] == "completed" else RED
            status_text = f"[{color_text(task['status'].capitalize(), status_color)}]".ljust(22)
            print(f" {index}. {status_text} {task['task']}")

        if mode == "main":
            print("\n\n [C] Create Task  [D] Delete Task [T] Toggle Status [B] Go Back\n")
        else:
            action_text = "Delete Task" if mode == "delete" else "Toggle Status"
            print(f"\n\n [{len(tasks) if len(tasks) == 1 else '1-' + str(len(tasks))}] {action_text}  [B] Go Back\n")
    else:
        print(" No tasks for this day.")
        print("\n\n [C] Create Task  [B] Go Back\n")


def handle_task_management(year, month, day):
    while True:
        clear_screen()
        display_task_for_day(year, month, day)
        action = input(" ").strip().lower()
        if action == "b":
            break
        elif action == "c":
            clear_screen()
            task_name = input(" Enter task: ").strip()
            if task_name:
                add_task(year, month, day, task_name)
        elif action in ["d", "t"]:
            tasks = get_tasks_for_day(year, month, day)
            if tasks:
                mode = "delete" if action == "d" else "toggle"
                while True:
                    clear_screen()
                    display_task_for_day(year, month, day, mode=mode)
                    task_index = input(" ").strip().lower()
                    if task_index == "b":
                        break
                    elif task_index.isdigit():
                        task_index = int(task_index) - 1
                        if 0 <= task_index < len(tasks):
                            if mode == "delete":
                                delete_task(year, month, day, task_index)
                                tasks = get_tasks_for_day(year, month, day)
                                if not tasks:
                                    break
                            else:
                                toggle_status(year, month, day, task_index)
