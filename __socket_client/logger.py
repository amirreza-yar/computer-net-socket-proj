import time
import colorama
from colorama import Fore

colorama.init(autoreset=True)

def log(message, level="INFO", source="General", function=""):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    log_levels = {
        "INFO": Fore.GREEN,
        "DEBUG": Fore.BLUE,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED
    }

    color = log_levels.get(level, Fore.WHITE)

    formatted_message = f"[{level}] [{function}]: {message}"

    print(color + formatted_message)