from utils.display_menu import *
from utils.display_title import *
from utils.database_commands import *
from colorama import Fore
from main import start_bot_menu

async def main_menu():
    while True:
        display_title()
        display_menu("Main Menu", ["Start Bot", "Settings", "Exit"], Fore.MAGENTA)
        choice = input("\n--> ")
        await process_main_menu_choice(choice)

async def process_main_menu_choice(choice):
    if choice == "1":
        await start_bot_menu()
    elif choice == "2":
        await settings_menu()
    elif choice == "3":
        print(Fore.YELLOW + "Exiting...")
        sys.exit(0)
    else:
        print(Fore.RED + "Invalid choice, please try again.")
        input("Press Enter to continue...")

async def settings_menu():
    while True:
        display_menu("Settings Menu", ["Add a new server", "View all servers", "Delete all servers", "Delete a server by ID", "Back to Main Menu"], Fore.BLUE)
        choice = input("\n---> ")
        if choice == "5":
            return
        await process_settings_menu_choice(choice)

async def process_settings_menu_choice(choice):
    if choice == "1":
        await add_new_server()
    elif choice == "2":
        await view_all_servers()
    elif choice == "3":
        await delete_all_server()
    elif choice == "4":
        server_id = input("Enter the ID of the server you want to delete: ")
        delete_server_by_id(server_id)
    else:
        print(Fore.RED + "Invalid choice, please try again.")
        input("Press Enter to continue...")