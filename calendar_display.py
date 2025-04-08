import calendar
import datetime
from task_manager import get_tasks_for_day, handle_task_management
from utils import color_text, BLUE, GREEN, RED, WHITE


def display_calendar(year, month):
    """
    Displays a calendar for a given month and year, highlighting the current day and showing task statuses.

    Args:
        year (int): The year to display the calendar for.
        month (int): The month to display the calendar for.
    """
    cal = calendar.monthcalendar(year, month)
    today = datetime.date.today()

    calendar_lines = [f"    {calendar.month_name[month]} {year}", " Mo Tu We Th Fr Sa Su"]
    todays_tasks = []

    for week in cal:
        line = ""
        for day in week:
            tasks = get_tasks_for_day(year, month, day)
            if day == 0:
                line += "   "
            elif day == today.day and month == today.month and year == today.year:
                todays_tasks = [task for task in tasks]
                line += f" {color_text(f'{day:2d}', BLUE)}"
            elif tasks:
                pending_tasks = sum(1 for task in tasks if task["status"] == "pending")
                color = GREEN if pending_tasks == 0 else RED
                line += f" {color_text(f'{day:2d}', color)}"
            else:
                line += f" {day:2d}"

        calendar_lines.append(line)

    legend_lines = [
        "",
        "",
        f"{color_text('Blue', BLUE)} - Current Day",
        f"{color_text('White', WHITE)} - Free Day",
        f"{color_text('Green', GREEN)} - Tasks Completed",
        f"{color_text('Red', RED)} - Tasks Pending"
    ]

    print()
    for i in range(len(calendar_lines)):
        legend_line = legend_lines[i] if i < len(legend_lines) else ""
        print(f"{calendar_lines[i]}      {legend_line}")

    if todays_tasks:
        print("\n\n " + color_text("Today's Checklist:", '4') + "\n")
        for task in todays_tasks:
            status_color = GREEN if task["status"] == "completed" else RED
            print(f" {color_text(task['task'], status_color)}")

    nav_line = f"\n\n [{color_text('1-' + str(calendar.monthrange(year, month)[1]), WHITE)}] Check Day " \
               f"[{color_text('N', WHITE)}] Next Month [{color_text('P', WHITE)}] Previous Month "

    today = datetime.date.today()
    if year != today.year or month != today.month:
        nav_line += f"[{color_text('C', WHITE)}] Current Month "

    nav_line += f"[{color_text('Q', WHITE)}] Quit\n"
    print(nav_line)


def go_to_next_month(current_date):
    """
    Returns the first day of the next month based on the current date.

    Args:
        current_date (datetime.date): The current date.

    Returns:
        datetime.date: The first day of the next month.
    """
    return (current_date.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)


def go_to_previous_month(current_date):
    """
    Returns the first day of the previous month based on the current date.

    Args:
        current_date (datetime.date): The current date.

    Returns:
        datetime.date: The first day of the previous month.
    """
    return (current_date.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)


def go_to_current_month():
    """
    Returns the first day of the current month.
    """
    today = datetime.date.today()
    return today.replace(day=1)


def handle_calendar_navigation(current_date):
    """
    Handles user navigation for the calendar: check day, go to next/previous/current month, or quit.

    Args:
        current_date (datetime.date): The current date to display in the calendar.

    Returns:
        datetime.date: The updated date after navigation.
    """
    display_calendar(current_date.year, current_date.month)
    action = input(" ").strip().lower()

    actions = {
        "n": lambda: go_to_next_month(current_date),
        "p": lambda: go_to_previous_month(current_date),
        "c": lambda: go_to_current_month()
        if (current_date.year, current_date.month) != (datetime.date.today().year, datetime.date.today().month)
        else current_date,
        "q": exit
    }

    if action.isdigit():
        day = int(action)
        last_day = calendar.monthrange(current_date.year, current_date.month)[1]
        if 1 <= day <= last_day:
            handle_task_management(current_date.year, current_date.month, day)
        return current_date

    return actions.get(action, lambda: current_date)()
