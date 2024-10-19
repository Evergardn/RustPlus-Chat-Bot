import math

async def calc_decay(args, rust_socket):
    if len(args) < 3:
        await rust_socket.send_team_message("Command usage: !calc decay {material} {value}")
        return

    decay_material = args[1]
    try:
        decay_value = int(args[2])
    except ValueError:
        await rust_socket.send_team_message("Error: Value must be a number.")
        return

    decay_calculations = {
        "wood": 83,
        "stone": 100,
        "metal": 125,
        "hqm": 166,
    }

    if decay_material in decay_calculations:
        decay_time = decay_value / decay_calculations[decay_material]
        await rust_socket.send_team_message(f"{math.trunc(decay_time / 1.66666666666 * 100)} minutes till decay")
    else:
        await rust_socket.send_team_message("Error: Invalid material specified. Please use {wood, stone, metal, hqm}.")
