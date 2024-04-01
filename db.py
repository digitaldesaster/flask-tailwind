import sqlite3
import json
from datetime import datetime

DATABASE_PATH = 'database.db'

def with_db_connection(func):
    """
    Decorator to manage database connections for any function that needs it.
    This version explicitly checks for a 'conn' keyword argument and inserts the
    connection if it's not provided, allowing for nested use of the decorator.
    """
    def inner(*args, **kwargs):
        if 'conn' not in kwargs:
            with sqlite3.connect(DATABASE_PATH) as conn:
                kwargs['conn'] = conn
                return func(*args, **kwargs)
        else:
            return func(*args, **kwargs)
    return inner

@with_db_connection
def execute_db_query(query, params=(), fetchone=False, conn=None):
    """
    Execute a database query and optionally fetch one result.
    """
    cursor = conn.cursor()
    cursor.execute(query, params)
    if fetchone:
        return cursor.fetchone()
    return cursor.fetchall()

@with_db_connection
def update_chat_entry(username, chat_started, messages, conn=None):
    query = "SELECT id FROM chat_history WHERE username = ? AND chat_started = ?"
    result = execute_db_query(query, (username, chat_started), fetchone=True, conn=conn)
    
    if result:
        entry_id = result[0]
        update_query = "UPDATE chat_history SET messages = ? WHERE id = ?"
        execute_db_query(update_query, (messages, entry_id), conn=conn)
        return True
    else:
        save_chat_db(username, chat_started, messages, conn=conn)
        return False

@with_db_connection
def save_chat_db(username, chat_started, messages, conn=None):
    query = "INSERT INTO chat_history (username, chat_started, messages) VALUES (?, ?, ?)"
    execute_db_query(query, (username, chat_started, messages), conn=conn)

@with_db_connection
def ensure_users_table_exists(conn=None):
    """
    Ensure the users table exists in the database.
    """
    create_table_query = '''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                username TEXT UNIQUE,
                                password_hash TEXT
                            )'''
    execute_db_query(create_table_query, conn=conn)

@with_db_connection
def ensure_chat_history_table_exists(conn=None):
    """
    Ensure the chat_history table exists in the database.
    """
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY,
            username TEXT,
            chat_started TIMESTAMP,
            messages TEXT
        )
    '''
    execute_db_query(create_table_query, conn=conn)

@with_db_connection
def get_user(username, conn=None):
    """
    Retrieve a user by username.
    """
    return execute_db_query("SELECT username, password_hash FROM users WHERE username=?", (username,), fetchone=True, conn=conn)

@with_db_connection
def add_user(username, password_hash, conn=None):
    """
    Add a new user to the database.
    """
    execute_db_query("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash), conn=conn)

@with_db_connection
def list_chat_history(conn=None):
    """
    List all chat history records sorted by the newest first.
    """
    query = "SELECT username, chat_started, messages FROM chat_history ORDER BY chat_started DESC"
    results = execute_db_query(query, conn=conn)
    
    # Convert the results into a list of dictionaries
    chat_history_list = [
        {
            "username": row[0],
            "chat_started": row[1],  # Convert timestamp to readable format
            "display_date": datetime.fromtimestamp(row[1]).strftime('%d.%m.%Y %H:%M'),
            "messages": json.loads(row[2])
        } for row in results
    ]
    
    # Convert the list of dictionaries into a JSON array string
    return chat_history_list

@with_db_connection
def get_chat_messages(username, chat_started, conn=None):
    query = "SELECT messages FROM chat_history WHERE username=? AND chat_started=?"
    result = execute_db_query(query, (username, chat_started), fetchone=True, conn=conn)
    if result:
        return result[0]
    else:
        return "No messages found for the given parameters."

@with_db_connection
def delete_all_chat_history(conn=None):
    """
    Delete all chat history records.
    """
    query = "DELETE FROM chat_history"
    execute_db_query(query, conn=conn)  

# Ensure tables exist and the database connection setup remains unchanged from the previous setup.
ensure_users_table_exists()
ensure_chat_history_table_exists()
#delete_all_chat_history()