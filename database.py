import sqlite3

def setup_database():
    """
    Sets up the SQLite database, creates the users table if it doesn't exist,
    and adds some initial data.
    """
    # Using a file-based database named 'users.db'
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    """
    )

    # Add some initial data if the table is empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        initial_users = [
            ("Alice", "alice@wonderland.io"),
            ("Charlie", "charlie@factory.com"),
        ]
        cursor.executemany(
            "INSERT INTO users (name, email) VALUES (?, ?)", initial_users
        )
        print("Database initialized and seeded with initial users.")

    conn.commit()
    return conn