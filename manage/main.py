import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import rustplus
except ImportError:
    install("rustplus")

try:
    from dotenv import load_dotenv
except ImportError:
    install("python-dotenv")

from rustplus import *
from server_lists import get_all_servers, get_server_by_steamid
import asyncio, json, math, os
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

steam_id = os.getenv('steamid')
server_data = get_server_by_steamid(steam_id)
desired_marker_types = {4, 5, 6, 8}

if server_data:
    name = server_data['name']
    ip = server_data['ip']
    port = server_data['port']
    playerId = server_data['playerId']
    playerToken = server_data['playerToken']

def get_cctv():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'manage', 'cctv.json')
    
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
        type_chinook = "Chinook incoming"
        return type_chinook
    elif marker_type == 5:
        type_cargo = "Cargo Ship spotted"
        return type_cargo
    elif marker_type == 6:
        type_crate = "Crate detected"
        return type_crate
    elif marker_type == 8:
        type_heli = "Patrol Helicopter in the area"
        return type_heli
    else:
        return "Unknown marker"

async def Main():
    options = CommandOptions(prefix="!")
    server_details = ServerDetails(ip, port, playerId, playerToken)
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
    async def seed(command: ChatCommand):
        await rust_socket.send_team_message("The seed is " + str((await rust_socket.get_info()).seed))

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
    async def calc(command: Command):
        args = [arg.lower() for arg in command.args]

        # if args[0] == "craft":
        #     print(args[0])

        # elif args[0] == "rec":
        #     print(args[0])

        if args[0] == "decay":
            if len(args) >= 3:
                decay_material = args[1]
                decay_value = args[2]

                if decay_material == "wood":
                    x = int(decay_value) / 83
                    result = round(x, 2)
                    await rust_socket.send_team_message(str(math.trunc(x/1.66666666666*100 )) + " minutes till decay")

                elif decay_material == "stone":
                    x = int(decay_value) / 100
                    result = round(x, 2)
                    await rust_socket.send_team_message(str(math.trunc(x/1.66666666666*100)) + " minutes till decay")

                elif decay_material == "metal":
                    x = int(decay_value) / 125
                    result = round(x, 2)
                    await rust_socket.send_team_message(str(math.trunc(x/1.66666666666*100 )) + " minutes till decay")

                elif decay_material == "hqm":
                    x = int(decay_value) / 166
                    
                    await rust_socket.send_team_message(str(math.trunc(x/1.66666666666*100)) + " minutes till decay")

            else:
                await rust_socket.send_team_message("Command usage: !calc decay [material] [value]")
        else:
            await rust_socket.send_team_message("This is not a valid argument, try [decay]")

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
    
    async def log_team_chat():
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            log_file_path = os.path.join(base_dir, 'files', 'team_chat.txt')

            os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

            messages = await rust_socket.get_team_chat()

            with open(log_file_path, 'a') as f:
                for message in messages:
                    readable_time = datetime.fromtimestamp(message.time, timezone.utc).strftime('%Y-%m-%d : %H:%M:%S')
                    log_entry = f"{readable_time} - {message.name}: {message.message}\n"
                    f.write(log_entry)

            print("Team chat messages have been logged.")
                
        except Exception as e:
            print(f"An error occurred: {e}")

    async def events():
        markers = await rust_socket.get_markers()
        filtered_markers = [marker for marker in markers if marker.type in desired_marker_types]
        
        for marker in filtered_markers:
            message = get_marker_message(marker.type)
            await rust_socket.send_team_message(f"Event was found: {message}!")

    asyncio.create_task(log_team_chat())
    asyncio.create_task(nightDay())
    asyncio.create_task(events())

    await rust_socket.hang()

asyncio.run(Main())