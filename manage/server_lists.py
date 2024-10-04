from dotenv import load_dotenv
import os

load_dotenv()

steam_id = os.getenv('steamid')

servers = [
    {
        "name": "Rustafied.com - EU Long",
        "ip": "64.40.9.31",
        "port": "28017",
        "playerId": steam_id,
        "playerToken": "your token here",
    },
    {
        "name": "Rustafied.com - EU Long III",
        "ip": "195.60.166.130",
        "port": "28017",
        "playerId": steam_id,
        "playerToken": "your token here",
    },
]

def get_all_servers():
    return servers

def get_server_by_steamid(steam_id):
    for server in servers:
        if server['playerId'] == steam_id:
            return server
    return None