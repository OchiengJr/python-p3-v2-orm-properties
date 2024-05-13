import sqlite3

# Define the database filename
DATABASE_NAME = 'company.db'

def initialize_database():
    """
    Initialize the SQLite database connection and cursor.

    Returns:
        tuple: A tuple containing the database connection and cursor.
    """
    try:
        # Establish a connection to the database
        conn = sqlite3.connect(DATABASE_NAME)
        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()
        return conn, cursor
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
        # If an error occurs, return None for both connection and cursor
        return None, None

# Initialize the database connection and cursor
CONN, CURSOR = initialize_database()

# Ensure that the connection and cursor are valid
if CONN is None or CURSOR is None:
    # If initialization failed, raise an error
    raise RuntimeError("Failed to initialize database connection and cursor")

# Optionally, you can define a function to close the database connection
def close_database():
    """
    Close the SQLite database connection.
    """
    try:
        CONN.close()
        print("Database connection closed successfully")
    except sqlite3.Error as e:
        print(f"Error closing database connection: {e}")

# Optionally, you can use a context manager to handle database connection
# with initialize_database() as (CONN, CURSOR):
#     # Perform database operations using CURSOR

# Module-level documentation
__doc__ = """
This module provides functions to initialize and manage the SQLite database connection and cursor.
"""

