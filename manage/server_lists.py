servers = [
    {
        "name": "Rustafied.com - EU Long",
        "ip": "64.40.9.31",
        "port": "28017",
        "playerId": "76561199163964082",
        "playerToken": "422692958"
    },
    {
        "name": "Rustafied.com - EU Long III",
        "ip": "195.60.166.130",
        "port": "28017",
        "playerId": "76561199163964082",
        "playerToken": "-2095244273",
    },
]

def get_all_servers():
    return servers

def get_server_by_steamid(steam_id):
    for server in servers:
        if server['playerId'] == steam_id:
            return server
    return None