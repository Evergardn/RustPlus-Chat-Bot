from colorama import init, Fore
import logging
from datetime import datetime

def log_error(exception):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    error_message = f"Error: {str(exception)}"
    logging.error(f"{current_time} - {error_message}")
    print(Fore.RED + f"[{current_time}] {error_message}")