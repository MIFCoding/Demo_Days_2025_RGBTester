from config import *

# ANSI цветовые коды
COLOR_RESET = "\033[0m"
COLOR_RED = "\033[31m"
COLOR_GREEN = "\033[32m"
COLOR_YELLOW = "\033[33m"
COLOR_BLUE = "\033[34m"
COLOR_MAGENTA = "\033[35m"
COLOR_CYAN = "\033[36m"
COLOR_WHITE = "\033[37m"
COLOR_BOLD = "\033[1m"
COLOR_PINK = '\033[95m'

# Уровни сложности и их цвета
if RAINBOW_MODE:
    DIFFICULTY_COLORS = {
        "": COLOR_WHITE,
        "легкий": COLOR_GREEN,
        "средний": COLOR_YELLOW,
        "тяжелый": COLOR_MAGENTA,
        "экстремальный": COLOR_RED
    }
else:
    DIFFICULTY_COLORS = {
        "": COLOR_WHITE,
        "легкий": COLOR_WHITE,
        "средний": COLOR_WHITE,
        "тяжелый": COLOR_WHITE,
        "экстремальный": COLOR_WHITE
    }

def display_heart():
    COLOR_PINK = '\033[95m'
    COLOR_RESET = '\033[0m'
    
    heart = [
        COLOR_PINK + "     _____     _____      " + COLOR_RESET,
        COLOR_PINK + "    /♥♥♥♥♥\\_ _/♥♥♥♥♥\\   " + COLOR_RESET,
        COLOR_PINK + "  /♥♥♥♥♥♥♥♥♥ ♥♥♥♥♥♥♥♥♥\\  " + COLOR_RESET,
        COLOR_PINK + " |♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥|  " + COLOR_RESET,
        COLOR_PINK + " |♥♥♥♥" + COLOR_BOLD + f"| {COLOR_RED}R{COLOR_GREEN}G{COLOR_BLUE}B{COLOR_WHITE}Tester {COLOR_PINK}|" + COLOR_RESET + COLOR_PINK + "♥♥♥♥|" + COLOR_RESET,
        COLOR_PINK + "  \\♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥/  " + COLOR_RESET,
        COLOR_PINK + "    \\♥♥♥♥♥♥♥♥♥♥♥♥♥♥♥/    " + COLOR_RESET,
        COLOR_PINK + "     \\♥♥♥♥♥♥♥♥♥♥♥♥♥/     " + COLOR_RESET,
        COLOR_PINK + "       \\♥♥♥♥♥♥♥♥♥/       " + COLOR_RESET,
        COLOR_PINK + "         \\♥♥♥♥♥/         " + COLOR_RESET,
        COLOR_PINK + "           \\♥/           " + COLOR_RESET
    ]
    
    for line in heart:
        print(line, flush=False)
    
    print(f"\n{COLOR_BOLD}{COLOR_WHITE}Нажмите Enter чтобы продолжить...{COLOR_RESET}", flush=True)