from rustplus import *
import asyncio
from database.database import *
from colorama import Fore
from tabulate import tabulate
from utils.clear_console import clear_console
from utils.log_errors import log_error
from utils.display_menu import *
from utils.database_commands import *
from utils.message_utils import *
from events.events_handler import *
from commands.calculate_recycle import calc_scrap_rec
from commands.calculate_decay import calc_decay
from commands.basic_commands import *
from config import *

async def start_bot_menu():
    try:
        clear_console(keep_title=True)
        servers = get_all_servers()

        if not servers:
            print(Fore.RED + "No servers found, please add a server in Settings.")
            input("Press Enter to return to the menu...")
            return

        servers_table = []
        for idx, server in enumerate(servers, start=1):
            servers_table.append([idx, server[1], server[2], server[3], server[4], server[5]])

        headers = ["Name", "IP", "Port", "ID", "Token"]
        print(Fore.GREEN + "\nAvailable Servers:\n")
        print(Fore.GREEN + tabulate(servers_table, headers, tablefmt="fancy_grid"))

        server_choice = get_server_choice(servers_table)

        if server_choice is None:
            print(Fore.RED + "Invalid choice. Please try again.")
            input("Press Enter to return to the menu...")
            return

        selected_server = servers[server_choice - 1]
        await start_bot_for_server(selected_server)

    except Exception as e:
        log_error(e)


async def start_bot_for_server(selected_server):
    print(f"\nStarting the bot for server: {selected_server[1]}")
    
    server_details = ServerDetails(
        selected_server[2],  # IP
        selected_server[3],  # Port
        selected_server[4],  # Player ID
        selected_server[5]   # Player Token
    )

    options = CommandOptions(prefix="!")
    rust_socket = RustSocket(server_details, command_options=options)

    await rust_socket.connect()
    await rust_socket.send_team_message("Bot connected.")

    @Command(server_details, aliases=['help', 'h'])
    async def help_command(command: ChatCommand):
        await help(rust_socket)

    @Command(server_details, aliases=['t', 'TIME', 'tm', 'TM'])
    async def time_command(command: ChatCommand):
        await time(rust_socket)

    @Command(server_details, aliases=['q', 'Q'])
    async def queue_command(command: ChatCommand):
        await queue(rust_socket)

    @Command(server_details, aliases=['p'])
    async def pop_command(command: ChatCommand):
        await pop(rust_socket)

    @Command(server_details)
    async def seed_command(command: ChatCommand):
        await seed(rust_socket)
    
    @Command(server_details, aliases=['codes'])
    async def codes_command(command: ChatCommand):
        await codes(command, rust_socket)

    @Command(server_details, aliases=['calc'])
    async def calc(command: ChatCommand):
        if await handle_help_request(command.args, rust_socket):
            return

        args = [arg.lower() for arg in command.args]

        if not args:
            await send_error_message("Error: No arguments provided. Type '!calc help' for usage details.", rust_socket)
            return

        command_type = args[0]

        command_handlers = {
            "rec": calc_scrap_rec,
            "decay": calc_decay,
        }

        if command_type in command_handlers:
            await command_handlers[command_type](args, rust_socket)
        else:
            await send_error_message("Error: Unknown command. Type '!calc help' for usage details.", rust_socket)


    asyncio.create_task(nightDay(rust_socket))
    asyncio.create_task(event(rust_socket))
    asyncio.create_task(log_team(rust_socket))

    await rust_socket.hang()