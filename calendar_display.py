import calendar
import datetime
from task_manager import get_tasks_for_day, handle_task_management


def display_calendar(year, month):
    cal = calendar.monthcalendar(year, month)
    today = datetime.date.today()

    calendar_lines = [f"    {calendar.month_name[month]} {year}", " Mo Tu We Th Fr Sa Su"]

    for week in cal:
        line = ""
        for day in week:
            tasks = get_tasks_for_day(year, month, day)
            if day == 0:
                line += "   "
            elif day == today.day and month == today.month and year == today.year:
                line += f" \033[1;1;34m{day:2d}\033[0m"
            elif tasks:
                pending_tasks = sum(1 for task in tasks if task["status"] == "pending")
                if pending_tasks == 0:
                    line += f" \033[1;32m{day:2d}\033[0m"
                else:
                    line += f" \033[1;31m{day:2d}\033[0m"
            else:
                line += f" {day:2d}"

        calendar_lines.append(line)

    legend_lines = [
        "",
        "",
        "\033[1;34mBlue\033[0m - Current Day",
        "\033[0mWhite - Free Day",
        "\033[1;32mGreen\033[0m - Tasks Completed",
        "\033[1;31mRed\033[0m - Tasks Pending"
    ]

    print()
    for i in range(len(calendar_lines)):
        legend_line = legend_lines[i] if i < len(legend_lines) else ""
        print(f"{calendar_lines[i]}      {legend_line}")

    print(f"\n\n [\033[1;97m1-{calendar.monthrange(year, month)[1]}\033[0m] Check Day  "
          f"[\033[1;97mN\033[0m] Next Month [\033[1;97mP\033[0m] Previous Month  [\033[1;97mQ\033[0m] Quit\n")


def go_to_next_month(current_date):
    return (current_date.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)


def go_to_previous_month(current_date):
    return (current_date.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)


def handle_calendar_navigation(current_date):
    display_calendar(current_date.year, current_date.month)
    action = input(" ").strip().lower()

    if action == 'n':
        return go_to_next_month(current_date)
    elif action == 'p':
        return go_to_previous_month(current_date)
    elif action == 'q':
        exit()
    elif action.isdigit():
        day = int(action)
        last_day_of_month = calendar.monthrange(current_date.year, current_date.month)[1]
        if 1 <= day <= last_day_of_month:
            handle_task_management(current_date.year, current_date.month, day)

    return current_date
