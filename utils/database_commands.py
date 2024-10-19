from colorama import Fore
from tabulate import tabulate
from database.database import *

async def add_new_server():
    name = input("Enter the server name: ")
    ip = input("Enter IP of the server: ")
    port = input("Enter PORT of the server: ")
    steam_id = input("Enter your SteamId: ")
    player_token = input("Enter Player Token: ")

    insert_server(name, ip, port, steam_id, player_token)
    print(Fore.GREEN + f"Server '{name}' has been added.")
    input("Press Enter to continue...")

async def view_all_servers():
    servers = get_all_servers()

    if not servers:
        print(Fore.RED + "No servers found.")
    else:
        headers = ["ID", "Name", "IP", "Port",   "PlayerID", "Token"]
        print(Fore.GREEN + tabulate(servers, headers, tablefmt="fancy_grid"))
    
    input("\n--> Press Enter to continue...")

async def delete_all_server():
    confirmation = input(Fore.RED + "Are you sure you want to delete all servers? (y/n): ").lower()
    if confirmation == 'y':
        delete_all_servers()
        print(Fore.GREEN + "All servers have been deleted.")
    else:
        print(Fore.YELLOW + "Operation cancelled.")
    input("Press Enter to continue...")

async def delete_server_b_id():
    server_id = int(input("Enter the server ID to delete: "))
    delete_server_by_id(server_id)
    print(Fore.GREEN + f"Server with ID {server_id} has been deleted.")
    input("Press Enter to continue...")