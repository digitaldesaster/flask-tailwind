import sqlite3

DATABASE_PATH = 'users.db'

def with_db_connection(func):
    """
    Decorator to manage database connections for any function that needs it.
    """
    def inner(*args, **kwargs):
        with sqlite3.connect(DATABASE_PATH) as conn:
            return func(conn, *args, **kwargs)
    return inner

@with_db_connection
def execute_db_query(conn, query, params=(), fetchone=False):
    """
    Execute a database query and optionally fetch one result.
    """
    cursor = conn.cursor()
    cursor.execute(query, params)
    if fetchone:
        return cursor.fetchone()
    return cursor.fetchall()

def ensure_users_table_exists():
    """
    Ensure the users table exists in the database.
    """
    create_table_query = '''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                username TEXT UNIQUE,
                                password_hash TEXT
                            )'''
    execute_db_query(create_table_query)

def get_user(username):
    return execute_db_query("SELECT username, password_hash FROM users WHERE username=?", (username,), fetchone=True)
def add_user(username,password_hash):
    execute_db_query("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
