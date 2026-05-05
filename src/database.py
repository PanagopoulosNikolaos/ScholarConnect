import sqlite3
from pathlib import Path

def getConnection():
    """
    Establishes a connection to the SQLite database.

    Returns:
        sqlite3.Connection: The active database connection.
    """
    db_path = Path("db/scholarconnect.sqlite3")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row # Allows accessing columns by name.
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
