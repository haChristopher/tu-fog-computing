"""
    Helper functions to connect to SQLite database,
    and store pending messages.
"""
import sqlite3
import logging as log


def create_connection(db_file: str):
    try:
        conn = sqlite3.connect(db_file)
        log.info(f"Connected to SQLite with name: {db_file}")
        return conn
    except sqlite3.Error as e:
        log.error(e)

    return None

def setup_table(conn: sqlite3.Connection):
    try:
        c = conn.cursor()
        c.execute(
            '''CREATE TABLE IF NOT EXISTS messages
                     (id INTEGER PRIMARY KEY, message json, send BOOLEAN, city text, Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
            ''')
        conn.commit()
        log.info("Created table messages")
    except sqlite3.Error as e:
        log.error(e)

def write_information_to_db(conn: sqlite3.Connection, message_json, city):
    try:
        c = conn.cursor()
        c.execute(
            "INSERT INTO messages (message, send, city) VALUES (?, ?, ?)",
            (message_json, False, city)
        )
        conn.commit()
        log.info("Inserted message into table messages")
    except sqlite3.Error as e:
        log.error(e)

def get_all_information_for_city(conn: sqlite3.Connection, city):
    try:
        c = conn.cursor()
        c.execute(
            "SELECT id, message FROM messages WHERE city = ?",
            (city,)
        )
        rows = c.fetchall()
        return rows
    except sqlite3.Error as e:
        log.error(e)
        return None
    
def delete_messages_by_ids(conn: sqlite3.Connection, ids):
    try:
        c = conn.cursor()
        for id in ids:
            c.execute(
                "DELETE FROM messages WHERE id = ?",
                (id,)
            )
        conn.commit()
        log.info("Deleted messages from table messages")
    except sqlite3.Error as e:
        log.error(e)