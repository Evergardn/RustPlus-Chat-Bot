import sqlite3

def create_db():
    conn = sqlite3.connect('servers.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS servers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        ip TEXT NOT NULL,
        port TEXT NOT NULL,
        playerId TEXT NOT NULL,
        playerToken TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

def insert_server(name, ip, port, playerId, playerToken):
    conn = sqlite3.connect('servers.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO servers (name, ip, port, playerId, playerToken)
    VALUES (?, ?, ?, ?, ?)
    ''', (name, ip, port, playerId, playerToken))

    conn.commit()
    conn.close()

def get_all_servers():
    conn = sqlite3.connect('servers.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM servers')
    servers = cursor.fetchall()

    conn.close()
    return servers

def get_server_by_id(server_id):
    conn = sqlite3.connect('servers.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM servers WHERE id=?', (server_id,))
    server = cursor.fetchone()

    conn.close()
    return server

def delete_all_servers():
    conn = sqlite3.connect('servers.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM servers')

    conn.commit()
    conn.close()

def delete_server_by_id(server_id):
    conn = sqlite3.connect('servers.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM servers WHERE id=?', (server_id,))

    conn.commit()
    conn.close()
