BLUE = "1;34"
GREEN = "1;32"
RED = "1;31"
WHITE = "0"
UNDERLINE = "4"


def color_text(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"


def clear_screen():
    print("\033c")
