import json
from utils import clear_screen


def load_tasks():
    with open("tasks.json", "r") as f:
        return json.load(f)


def save_tasks(tasks):
    with open("tasks.json", 'w') as f:
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
        task['status'] = 'completed' if task['status'] == 'pending' else 'pending'

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
    print(f"\n \033[4m{year}-{month:02d}-{day:02d}\033[0m:\n")

    if tasks:
        for index, task in enumerate(tasks, start=1):
            status_color = "\033[1;32m" if task['status'] == "completed" else "\033[1;31m"
            status_text = f"[{status_color}{task['status'].capitalize()}\033[0m]".ljust(22)
            print(f" {index}. {status_text} {task['task']}")

        if mode == "main":
            print("\n\n [\033[1;97mC\033[0m] Create Task  [\033[1;97mD\033[0m] Delete Task "
                  "[\033[1;97mT\033[0m] Toggle Status [\033[1;97mB\033[0m] Go Back\n")
        else:
            action_text = "Delete Task" if mode == "delete" else "Toggle Status"
            print(f"\n\n [{len(tasks) if len(tasks) == 1 else '1-' + str(len(tasks))}] "
                  f"{action_text}  [\033[1;97mB\033[0m] Go Back\n")
    else:
        print(" No tasks for this day.")
        print("\n\n [\033[1;97mC\033[0m] Create Task  [\033[1;97mB\033[0m] Go Back\n")


def handle_task_management(year, month, day):
    while True:
        clear_screen()
        display_task_for_day(year, month, day)
        action = input(" ").strip().lower()

        if action == 'b':
            break
        elif action == 'c':
            clear_screen()
            task_name = input(" Enter task: ").strip()
            if task_name:
                add_task(year, month, day, task_name)
        elif action in ['d', 't']:
            tasks = get_tasks_for_day(year, month, day)
            if tasks:
                mode = "delete" if action == 'd' else "toggle"
                while True:
                    clear_screen()
                    display_task_for_day(year, month, day, mode=mode)
                    task_index = input(" ").strip().lower()

                    if task_index == 'b':
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
