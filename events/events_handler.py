import asyncio
from colorama import Fore
from utils.log_errors import log_error

desired_marker_types = {4, 5, 6, 8}

def get_marker_message(marker_type):
    messages = {
        4: "Chinook incoming",
        5: "Cargo Ship spotted",
        6: "Crate detected",
        8: "Patrol Helicopter in the area"
    }
    return messages.get(marker_type, "Unknown marker")

async def nightDay(rust_socket):
    print(Fore.GREEN + "\n- Night/Day tracking started")
    
    night_start_time = 17.65
    day_start_time = 23.90
    
    last_state = None

    while True:
        try:
            response = await rust_socket.get_time()
            
            if response is None:
                log_error("rust_socket.get_time() returned None")
                await asyncio.sleep(1)
                continue
            
            currentTime = round(response.raw_time, 2)
            
            if night_start_time <= currentTime < day_start_time and last_state != 'night':
                await rust_socket.send_team_message(f">>> 5 mins before Night")
                last_state = 'night'

            elif currentTime >= day_start_time and last_state != 'day':
                await rust_socket.send_team_message(">>> 5 mins before Day")
                last_state = 'day'

            await asyncio.sleep(1)

        except AttributeError as e:
            log_error(f"AttributeError: {e}")
            await asyncio.sleep(1)
    
        except Exception as e:
            log_error(f"General Exception: {e}")
            await asyncio.sleep(1)


# async def log_team_chat(rust_socket):
#     base_dir = os.path.dirname(os.path.abspath(__file__))
#     log_file_path = os.path.join(base_dir, 'files', 'team_chat.txt')
#     os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

#     messages = await rust_socket.get_team_chat()

#     with open(log_file_path, 'a') as f:
#         for message in messages:
#             if not message.message.startswith('!'):
#                 readable_time = datetime.fromtimestamp(message.time, timezone.utc).strftime('%Y-%m-%d : %H:%M:%S')
#                 f.write(f"{readable_time} - {message.name}: {message.message}\n")

#     print(Fore.GREEN + "- Team chat messages have been logged.")

# Team handler
async def log_team(rust_socket):
    print(Fore.GREEN + '- Team logging socket started')
    previous_online_status = {}
    previous_alive_status = {}

    while True:
        info = await rust_socket.get_team_info()

        await process_team_info(info, rust_socket, previous_online_status, previous_alive_status)

        await asyncio.sleep(5)

async def process_team_info(info, rust_socket, previous_online_status, previous_alive_status):
    for member in info.members:
        steam_id = member.steam_id

        if is_new_member(steam_id, previous_online_status):
            initialize_member_status(steam_id, member, previous_online_status, previous_alive_status)
        else:
            await handle_status_changes(member, rust_socket, previous_online_status, previous_alive_status)

def is_new_member(steam_id, previous_online_status):
    return steam_id not in previous_online_status

def initialize_member_status(steam_id, member, previous_online_status, previous_alive_status):
    previous_online_status[steam_id] = member.is_online
    previous_alive_status[steam_id] = member.is_alive

async def handle_status_changes(member, rust_socket, previous_online_status, previous_alive_status):
    steam_id = member.steam_id

    if has_online_status_changed(steam_id, member, previous_online_status):
        await notify_online_status_change(member, rust_socket)
        previous_online_status[steam_id] = member.is_online

    if has_alive_status_changed(steam_id, member, previous_alive_status):
        await rust_socket.send_team_message(f">>> {member.name} is dead.")
        previous_alive_status[steam_id] = member.is_alive

def has_online_status_changed(steam_id, member, previous_online_status):
    return previous_online_status[steam_id] != member.is_online

def has_alive_status_changed(steam_id, member, previous_alive_status):
    return previous_alive_status[steam_id] != member.is_alive and not member.is_alive

async def notify_online_status_change(member, rust_socket):
    if member.is_online:
        await rust_socket.send_team_message(f">>> Player {member.name} connected to the game!")
    else:
        await rust_socket.send_team_message(f">>> Player {member.name} quit the game!")

# Event handler
async def event(rust_socket):
    print(Fore.GREEN + '- Event tracking started')
    processed_marker_ids = set()

    while True:
        try:
            markers = await rust_socket.get_markers()
            filtered_markers = [marker for marker in markers if marker.type in desired_marker_types]

            new_messages = []
            for marker in filtered_markers:
                if marker.id not in processed_marker_ids:
                    message = get_marker_message(marker.type)
                    new_messages.append(message)
                    processed_marker_ids.add(marker.id)
            
            if new_messages:
                combined_message = " /// ".join(new_messages)
                await rust_socket.send_team_message(f">>> {combined_message}!")
            
            await asyncio.sleep(1)

        except Exception as e:
            log_error(e)
            await asyncio.sleep(1)