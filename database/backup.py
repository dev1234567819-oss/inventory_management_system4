"""
Simple database backup utility.
Exports all tables to SQL dump files under reports/backups/.
"""

import os
import datetime
from database.db_connection import connect_db
import config


def backup_database(output_dir=None):
    """
    Create a basic SQL dump of all application tables.
    Returns the path to the generated backup file, or None on failure.
    """
    if output_dir is None:
        output_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "reports",
            "backups",
        )
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(output_dir, f"inventory_backup_{timestamp}.sql")

    conn = connect_db()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        tables = ["users", "products", "suppliers", "purchases", "sales"]
        lines = [
            f"-- Inventory Management System Backup",
            f"-- Generated: {datetime.datetime.now().isoformat()}",
            f"-- Database: {config.DB_NAME}",
            "",
            f"USE {config.DB_NAME};",
            "",
        ]

        for table in tables:
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            cols = [d[0] for d in cursor.description] if cursor.description else []

            lines.append(f"-- Table: {table}")
            lines.append(f"DELETE FROM {table};")
            for row in rows:
                values = []
                for v in row:
                    if v is None:
                        values.append("NULL")
                    elif isinstance(v, (int, float)):
                        values.append(str(v))
                    else:
                        escaped = str(v).replace("\\", "\\\\").replace("'", "\\'")
                        values.append(f"'{escaped}'")
                col_list = ", ".join(cols)
                val_list = ", ".join(values)
                lines.append(f"INSERT INTO {table} ({col_list}) VALUES ({val_list});")
            lines.append("")

        with open(backup_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        cursor.close()
        conn.close()
        return backup_path
    except Exception as e:
        print(f"Backup failed: {e}")
        if conn:
            conn.close()
        return None


if __name__ == "__main__":
    path = backup_database()
    if path:
        print(f"Backup saved to: {path}")
    else:
        print("Backup failed.")
