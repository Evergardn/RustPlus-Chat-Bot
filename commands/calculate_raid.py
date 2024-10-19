import json, os
from utils.data_loader import load_data

async def calc_raid(args, rust_socket):
    data = load_data()

    if len(args) < 4:
        await rust_socket.send_team_message("Command usage: !calc raid {count_structure} {structure_name} {structure_health}")
        return

    try:
        count_structure = int(args[1])
    except ValueError:
        await rust_socket.send_team_message("Error: Count must be a number.")
        return

    what_to_raid = " ".join(args[2:-1])
    try:
        health = int(args[-1])
    except ValueError:
        await rust_socket.send_team_message("Error: Health must be a number.")
        return

    raid_data = data.get("raid_data", {})

    if what_to_raid not in raid_data:
        await rust_socket.send_team_message(f"Error: '{what_to_raid}' is not a valid structure to raid.")
        return

    structure_data = raid_data[what_to_raid]
    best_option = None
    lowest_cost = float('inf')

    for explosive_type, stats in structure_data.items():
        if isinstance(stats, dict):
            damage = stats["damage"]
            sulfur_per_unit = stats["sulfur"]

            explosive_needed = (health + damage - 1) // damage
            total_sulfur_cost = explosive_needed * sulfur_per_unit * count_structure

            if total_sulfur_cost < lowest_cost:
                best_option = (explosive_needed * count_structure, explosive_type)
                lowest_cost = total_sulfur_cost
        else:
            continue

    if best_option:
        result_message = f"Best option to raid {count_structure}x {what_to_raid}: {best_option[0]}x {best_option[1]} - {lowest_cost} sulfur total."
        await rust_socket.send_team_message(result_message)
    else:
        await rust_socket.send_team_message("Error: No valid raid options found.")
