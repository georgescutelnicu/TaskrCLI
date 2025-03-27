import datetime
from calendar_display import handle_calendar_navigation
from utils import clear_screen


def main():
    current_date = datetime.date.today()

    while True:
        clear_screen()
        current_date = handle_calendar_navigation(current_date)


if __name__ == "__main__":
    main()
