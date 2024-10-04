from rustplus import *
import asyncio, json, os, sys, subprocess
from datetime import datetime
from database import *

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
clear_console()

desired_marker_types = {4, 5, 6, 8}

def get_cctv():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'cctv.json')
    
    with open(file_path, 'r') as f:
        codes = json.load(f)
    
    LoilCodes = codes.get("LoilCodes", [])
    BanditCampCodes = codes.get("BanditCampCodes", [])
    DomeCodes = codes.get("DomeCodes", [])
    SiloCodes = codes.get("SiloCodes", [])
    OutpostCodes = codes.get("OutpostCodes", [])
    SmoilCodes = codes.get("SmoilCodes", [])

    return LoilCodes, BanditCampCodes, DomeCodes, SiloCodes, OutpostCodes, SmoilCodes


def get_marker_message(marker_type):
    unknown_marker_type = [1, 2, 3, 7]
        
    if marker_type == 4:
        return "Chinook incoming"
    elif marker_type == 5:
        return "Cargo Ship spotted"
    elif marker_type == 6:
        return "Crate detected"
    elif marker_type == 8:
        return "Patrol Helicopter in the area"
    else:
        return "Unknown marker"

def show_menu():
    print("\nMain Menu:")
    print("1. Start bot")
    print("2. Add new Server")
    print("3. Delete Server")
    print("4. View all valid Servers")
    return input("Choose the option: ")

def add_server():
    server_name = input("Enter server's name: ")
    server_ip = input("Enter server's ip: ")
    server_port = input("Enter server's port: ")
    player_id = input("Enter player's steam_id: ")
    player_token = input("Etner player's token: ")

    insert_server(server_name, server_ip, server_port, player_id, player_token)
    print(f"Server {server_name} successfully added.")
    clear_console()

def delete_server():
    servers = get_all_servers()
    
    if not servers:
        print("No servers to delete.")
        return
    
    print("\nAvailable servers:")
    for i, server in enumerate(servers):
        print(f"{i + 1}. {server[1]} (IP: {server[2]}, Port: {server[3]})")
    
    try:
        server_choice = int(input("Choose server to delete: ")) - 1
        if 0 <= server_choice < len(servers):
            delete_server_by_id(servers[server_choice][0])
            print(f"Server {servers[server_choice][1]} deleted.")
        else:
            print("Incorrect choice.")
    except ValueError:
        print("Please, enter the number.")

def show_servers():
    servers = get_all_servers()
    
    if not servers:
        print("Server are not founded.")
    else:
        print("\nAvailable servers:")
        for i, server in enumerate(servers):
            print(f"{i + 1}. {server[1]} (IP: {server[2]}, Port: {server[3]})")

async def start_bot():
    clear_console()
    create_db()
    servers = get_all_servers()
    
    if not servers:
        print("Server are not founded. Please, add new server.")
        return

    print("\nAvailable servers:")
    for i, server in enumerate(servers):
        print(f"{i + 1}. {server[1]} (IP: {server[2]}, Port: {server[3]})")

    try:
        server_choice = int(input("\nChoose the server to run bot: ")) - 1
        
        if server_choice < 0 or server_choice >= len(servers):
            print("Please, choose the available server.")
            return
        
        selected_server = servers[server_choice]
        print(f"\nRunnig bot for server: {selected_server[1]}")
    except ValueError:
        print("Incorrect input. Please, use only numbers.")
        return

    server_details = ServerDetails(
        selected_server[2],  # IP from the database
        selected_server[3],  # Port from the database
        selected_server[4],  # Player ID from the database
        selected_server[5]   # Player Token from the database
    )

    options = CommandOptions(prefix="!")
    rust_socket = RustSocket(server_details, command_options=options)

    await rust_socket.connect()
    await rust_socket.send_team_message("Bot connected and ready!")


    @Command(server_details)
    async def help(command: ChatCommand):
        await rust_socket.send_team_message("!help, !time, !queue, !pop, !seed, !team, !codes { }, !decay")


    @Command(server_details)
    async def time(command: ChatCommand):
        await rust_socket.send_team_message((await rust_socket.get_time()).time)

    @Command(server_details)
    async def queue(command: ChatCommand):
        await rust_socket.send_team_message("Currently " + str((await rust_socket.get_info()).queued_players) + " players in queue!")

    @Command(server_details)
    async def pop(command: ChatCommand):
        await rust_socket.send_team_message("Currently " + str((await rust_socket.get_info()).players) + " players connected!")

    @Command(server_details)
    async def codes(command: ChatCommand):
        Monument = str(command.args[0].lower())
        LoilCodes, BanditCampCodes, DomeCodes, SiloCodes, OutpostCodes, SmoilCodes = get_cctv()

        async def send_codes_as_single_message(codes):
            if codes:
                codes_message = ", ".join(codes)
                await rust_socket.send_team_message(codes_message)

        if Monument == "large":
            await send_codes_as_single_message(LoilCodes)

        elif Monument == "air":
            await rust_socket.send_team_message("AIRFIELDHELIPAD")

        elif Monument == "banditcamp":
            await send_codes_as_single_message(BanditCampCodes)

        elif Monument == "dome":
            await send_codes_as_single_message(DomeCodes)

        elif Monument == "silo":
            await send_codes_as_single_message(SiloCodes)

        elif Monument == "outpost":
            await send_codes_as_single_message(OutpostCodes)

        elif Monument == "smoil":
            await send_codes_as_single_message(SmoilCodes)

        elif Monument == "help":
            await rust_socket.send_team_message("help, smoil, loil, outpost, silo, dome, banditcamp, air")

        else:
            await rust_socket.send_team_message("This monument doesn't have camera codes or doesn't exist")

    @Command(server_details)
    async def team(command: ChatCommand):
        info = await rust_socket.get_team_info()

        for member in info.members:
            steam_id = member.steam_id
            name = member.name
            await rust_socket.send_team_message(f"Steam ID: {steam_id}, Name: {name}")

    async def nightDay():
        print("night/day tracked")
        isTime = True
        isTime2 = True

        day_message_sent = False

        while isTime or isTime2:
            currentTime = (await rust_socket.get_time()).raw_time
            currentTime = round(currentTime, 2)

            await asyncio.sleep(1)

            if currentTime == 17.65 and isTime:
                await rust_socket.send_team_message("It will be Night in 5 Minutes")
                isTime = False

            elif 23.90 <= currentTime <= 23.91 and isTime2 and not day_message_sent:
                await rust_socket.send_team_message("It will be Day in 5 Minutes")
                day_message_sent = True

    async def event():
        processed_marker_ids = set()

        try:
            while True:
                markers = await rust_socket.get_markers()
                filtered_markers = [marker for marker in markers if marker.type in desired_marker_types]

                for marker in filtered_markers:
                    if marker.id not in processed_marker_ids:
                        message = get_marker_message(marker.type)
                        await asyncio.sleep(2)
                        await rust_socket.send_team_message(f"Event was found: {message}!")

                        processed_marker_ids.add(marker.id)

                await asyncio.sleep(10)  # Check for new events every 10 seconds
        except Exception as e:
            print(f"An error occurred: {e}")

    asyncio.create_task(nightDay())
    asyncio.create_task(event())

    await rust_socket.hang()

async def main():
    while True:
        choice = show_menu()

        if choice == '1':
            await start_bot()
        elif choice == '2':
            add_server()
        elif choice == '3':
            delete_server()
        elif choice == '4':
            show_servers()
        else:
            print("Incorrect choice, please try again.")

if __name__ == "__main__":
    asyncio.run(main())