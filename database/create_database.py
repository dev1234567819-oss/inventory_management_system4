"""
Creates the inventory database and all required tables.
Run this script once before starting the application.
"""

import mysql.connector
from mysql.connector import Error
import config


def create_database_and_tables():
    """Create database (if missing) and all application tables."""
    try:
        # Connect without selecting a database first
        conn = mysql.connector.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            port=config.DB_PORT,
        )
        cursor = conn.cursor()
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {config.DB_NAME} "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        cursor.execute(f"USE {config.DB_NAME}")

        # Users table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(50) NOT NULL
            )
            """
        )

        # Products table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                brand VARCHAR(100),
                category VARCHAR(50),
                price DECIMAL(10,2) NOT NULL,
                quantity INT NOT NULL,
                image_path VARCHAR(255)
            )
            """
        )

        # Ensure optional columns exist (for upgrades)
        for col_name, col_type in [
            ("brand", "VARCHAR(100)"),
            ("image_path", "VARCHAR(255)"),
        ]:
            try:
                cursor.execute(f"ALTER TABLE products ADD COLUMN {col_name} {col_type}")
            except Error:
                pass  # column already exists

        # Suppliers table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS suppliers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                contact VARCHAR(50),
                email VARCHAR(100),
                address TEXT
            )
            """
        )

        # Purchases table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS purchases (
                id INT AUTO_INCREMENT PRIMARY KEY,
                item_name VARCHAR(100) NOT NULL,
                supplier_name VARCHAR(100),
                cost_price DECIMAL(10,2) NOT NULL,
                quantity INT NOT NULL,
                purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # Sales table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sales (
                id INT AUTO_INCREMENT PRIMARY KEY,
                item_name VARCHAR(100) NOT NULL,
                selling_price DECIMAL(10,2) NOT NULL,
                quantity_sold INT NOT NULL,
                total_revenue DECIMAL(10,2) NOT NULL,
                sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # Default admin user
        cursor.execute(
            "INSERT IGNORE INTO users (username, password) VALUES (%s, %s)",
            (config.DEFAULT_ADMIN_USERNAME, config.DEFAULT_ADMIN_PASSWORD),
        )

        conn.commit()
        cursor.close()
        conn.close()
        print(f"Database '{config.DB_NAME}' and tables created successfully.")
        return True
    except Error as e:
        print(f"Error creating database/tables: {e}")
        return False


if __name__ == "__main__":
    create_database_and_tables()
