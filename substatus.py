#!/usr/bin/env python3

import urllib.request
import datetime
import json
import sqlite3
from os.path import isfile as fileexists

SPACEAPI_DIRECTORY = "http://spaceapi.net/directory.json"
DATABASE = "space_states.db"

def open_db():
    return sqlite3.connect(DATABASE)

def create_db(conn):
    c = conn.cursor()
    c.execute(''' CREATE TABLE IF NOT EXISTS spaces (id INTEGER PRIMARY KEY, 
                                                    name text, url TEXT)''')
    c.execute(''' CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, 
                                                    space_id INTEGER,
                                                    time text, 
                                                    open INTEGER,
                                                    FOREIGN KEY(space_id) REFERENCES spaces(id) 
                                                    )''')
    with urllib.request.urlopen(SPACEAPI_DIRECTORY) as response:
        spaces = response.read()
    space_data = json.loads(spaces.decode("utf-8"))
    for line in space_data.items():
        c.execute(''' INSERT INTO spaces (name, url) VALUES (?, ?)''', (line[0], line[1]))

def close_db(conn):
    conn.commit()
    conn.close()

def get_states(conn):
    c = conn.cursor()
    spaces = c.execute('''SELECT * FROM spaces''').fetchall()
    for space in spaces:
        try:
            with urllib.request.urlopen(space[2], timeout=5) as response:
                state = response.read()
        except:
            continue

        #As sqlite does not support bools, we have to convert the state to int
        space_state = json.loads(state.decode("utf-8"))
        if (space_state.get("open") == True):
            space_open = 1
        else:
            space_open = 0

        #Write result to database
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("""INSERT INTO data (space_id, 
                                        time, 
                                        open) 
                    VALUES (?,?,?)""",
                                        (space[0],
                                            now,
                                            space_open))
        print(space[0], now, space_open)

if __name__ == "__main__":
    if not fileexists(DATABASE):
            conn = open_db()
            create_db(conn)
    else:
            conn = open_db()

    get_states(conn);
    close_db(conn)
