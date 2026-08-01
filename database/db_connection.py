"""
MySQL database connection module.
"""

import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
import config


def connect_db():
    """Establish and return a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME,
            port=config.DB_PORT,
        )
        return conn
    except Error as err:
        messagebox.showerror(
            "Database Error",
            f"Could not connect to database:\n{err}\n"
            f"Make sure '{config.DB_NAME}' exists and MySQL is running.",
        )
        return None


def get_cursor(conn, dictionary=False):
    """Return a cursor from the given connection."""
    if conn is None:
        return None
    return conn.cursor(dictionary=dictionary)
