"""os.path.join(

        HELP TIME QUEUE POP TEAM SEED CODES

"""
import asyncio
from utils.data_loader import get_cctv

async def time(rust_socket):
    await rust_socket.send_team_message((await rust_socket.get_time()).time)

async def help(rust_socket):
    await rust_socket.send_team_message("!help !time !queue !pop !seed <<>> !codes help !calc help")

async def queue(rust_socket):
    await rust_socket.send_team_message("Currently " + str((await rust_socket.get_info()).queued_players) + " players in queue!")

async def pop(rust_socket):
    await rust_socket.send_team_message("Currently " + str((await rust_socket.get_info()).players) + " players connected!")

async def seed(rust_socket):
    await rust_socket.send_team_message("The seed is " + str((await rust_socket.get_info()).seed))

async def codes(command, rust_socket):
        Monument = command.args[0].lower() if command.args else "help"
        cctv_codes = list(get_cctv())

        if not cctv_codes or len(cctv_codes) < 6:
            await rust_socket.send_team_message("CCTV codes data is missing or incomplete")
            return

        codes_map = {
            "large": cctv_codes[0] or ["No codes available for Large Oil"],
            "bandit": cctv_codes[1],
            "dome": cctv_codes[2],
            "silo": cctv_codes[3],
            "outpost": cctv_codes[4],
            "smoil": cctv_codes[5],
            "air": ["AIRFIELDHELIPAD"],
        }

        
        async def send_codes_as_single_message(codes):
            if codes:
                codes_message = ", ".join(codes)
                max_length = 80
                if len(codes_message) > max_length:
                    middle = len(codes) // 2
                    part1 = ", ".join(codes[:middle])
                    part2 = ", ".join(codes[middle:])
                    await rust_socket.send_team_message(part1)
                    await asyncio.sleep(1.5)
                    await rust_socket.send_team_message(part2)
                else:
                    await rust_socket.send_team_message(codes_message)
        if Monument == "help":
            await rust_socket.send_team_message("!codes [monument] | smoil, loil, outpost, silo, dome, banditcamp, air")
        elif Monument in codes_map:
            await send_codes_as_single_message(codes_map[Monument])
        else:
            await rust_socket.send_team_message("This monument doesn't have camera codes or doesn't exist")