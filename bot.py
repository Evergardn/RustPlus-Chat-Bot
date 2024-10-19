import asyncio
from config import setup_logging, setup_encoding, setup_colorama
from menus import main_menu
from utils.database_commands import create_db
from colorama import Fore

def main():
    setup_logging()
    setup_encoding()
    setup_colorama()
    create_db()

    try:
        asyncio.run(main_menu())
    except KeyboardInterrupt:
        print(Fore.YELLOW + "Bot is finishing work.")

if __name__ == "__main__":
    main()