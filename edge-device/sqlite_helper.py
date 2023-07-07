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
                     (id INTEGER PRIMARY KEY, message json, send BOOLEAN, send_attempt INTEGER ,Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
            ''')
        conn.commit()
        log.info("Created table messages")
    except sqlite3.Error as e:
        log.error(e)

def write_unsend_message(conn: sqlite3.Connection, message_json):
    try:
        c = conn.cursor()
        c.execute(
            "INSERT INTO messages (message, send, send_attempt) VALUES (?, ?, ?)",
            (message_json, False, 1)
        )
        conn.commit()
        log.info("Inserted message into table messages")
    except sqlite3.Error as e:
        log.error(e)

def get_next_unsend_message(conn: sqlite3.Connection):
    try:
        c = conn.cursor()
        c.execute(
            "SELECT id, message FROM messages WHERE send = ? order by Timestamp ASC LIMIT 1",
            (False,)
        )
        row = c.fetchone()
        if row is not None:
            id = row[0]
            message = row[1]
            return id, message
        else:
            return None, None
    except sqlite3.Error as e:
        log.error(e)

def increase_send_attempt(conn: sqlite3.Connection, id: int):
    try:
        c = conn.cursor()
        c.execute(
            "UPDATE messages SET send_attempt = send_attempt + 1 WHERE id = ?",
            (id,)
        )
        conn.commit()
        log.info(f"Increased send attempt for message with id: {id}")
    except sqlite3.Error as e:
        log.error(e)


def delete_all_send_message(conn: sqlite3.Connection):
    try:
        c = conn.cursor()
        c.execute(
            "DELETE FROM messages WHERE send = ?",
            (True,)
        )
        conn.commit()
        log.info("Deleted all send messages")
    except sqlite3.Error as e:
        log.error(e)


def mark_message_as_send(conn: sqlite3.Connection, id: int):
    try:
        c = conn.cursor()
        c.execute(
            "UPDATE messages SET send = ? WHERE id = ?",
            (True, id)
        )
        conn.commit()
        log.info(f"Marked message with id as send: {id}")
    except sqlite3.Error as e:
        log.error(e)