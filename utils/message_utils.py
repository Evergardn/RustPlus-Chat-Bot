async def send_help_message(rust_socket):
    help_message = (
        "!calc [decay/raid/rec] [arguments] | "
        "!calc scrap [safe/unsafe] [item] [amount]"
    )
    await rust_socket.send_team_message(help_message)

async def send_error_message(message, rust_socket):
    await rust_socket.send_team_message(message)

async def handle_help_request(args, rust_socket):
    if len(args) > 0 and args[0].lower() == "help":
        await send_help_message(rust_socket)
        return True
    return False
