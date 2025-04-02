BLUE = "1;34"
GREEN = "1;32"
RED = "1;31"
WHITE = "0"
UNDERLINE = "4"


def color_text(text, color_code):
    """
    Colorizes text using the specified color code.

    Args:
        text (str): The text to colorize.
        color_code (str): The color code to apply.

    Returns:
        str: The colorized text.
    """
    return f"\033[{color_code}m{text}\033[0m"


def clear_screen():
    """
    Clears the terminal screen.
    """
    print("\033c")
