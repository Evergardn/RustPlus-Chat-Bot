from .clear_console import clear_console
from colorama import Fore
import time, sys

def display_menu(title, options, color=Fore.GREEN):
    clear_console(keep_title=True)
    print(color + f"\n{title}:\n")
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")

def progress_bar(duration):
    for i in range(100):
        time.sleep(duration / 100)
        sys.stdout.write(f"\rProgress: [{'#' * (i // 2)}{' ' * (50 - i // 2)}] {i+1}%")
        sys.stdout.flush()
    print("\nOperation completed.")

def display_main_menu():
    print("\nMain Menu:\n")
    print(Fore.MAGENTA + "1. Start Bot")
    print(Fore.GREEN + "2. Settings")
    print(Fore.RED + "3. Exit")

def invalid_main_menu_choice():
    print("Invalid choice, please try again.")
    input("Press Enter to continue...")

def get_server_choice(servers):
    try:
        server_choice = int(input("\n--> "))
        if 1 <= server_choice <= len(servers):
            return server_choice
    except ValueError:
        return None

def display_available_servers(servers):
    print(Fore.GREEN + "\nAvailable Servers:\n")
    for i, server in enumerate(servers):
        print(f"{i + 1}. {server[1]} (IP: {server[2]}, Port: {server[3]})")

def invalid_server_choice():
    print(Fore.RED + "\nInvalid input. Please enter a valid number.")
    input("\nPress Enter to try again...")