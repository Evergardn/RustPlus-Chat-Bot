import json, os
from utils.data_loader import load_data

async def calc_scrap_rec(args, rust_socket):
    data = load_data()

    if len(args) < 4:
        await rust_socket.send_team_message("Command usage: !calc scrap {safe/unsafe} {item} {amount}")
        return

    scrap_data = data.get("scrap_data", {})
    item_mapping = data.get("item_mapping", {})
    zone_type, item_name, amount = args[1], args[2], args[3]

    if zone_type not in scrap_data:
        await rust_socket.send_team_message(f"Error: Invalid zone type '{zone_type}'. Use 'safe' or 'unsafe'.")
        return

    item_name = item_mapping.get(item_name, item_name)

    if item_name not in scrap_data[zone_type]:
        await rust_socket.send_team_message(f"Error: Invalid item '{item_name}'.")
        return

    item_data = scrap_data[zone_type][item_name]
    response_message = f"{amount}x {item_name.title()} in {zone_type} zone will give you:"

    for material, value_per_item in item_data.items():
        total_value = value_per_item * int(amount)
        response_message += f"\n- {total_value} {material}"

    await rust_socket.send_team_message(response_message)