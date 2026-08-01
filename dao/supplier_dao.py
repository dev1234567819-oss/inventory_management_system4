"""Data Access Object for suppliers."""

from database.db_connection import connect_db
from models.supplier import Supplier


class SupplierDAO:
    @staticmethod
    def get_all(query=""):
        """Return list of Supplier objects, optionally filtered."""
        conn = connect_db()
        suppliers = []
        if not conn:
            return suppliers
        try:
            cursor = conn.cursor()
            if query:
                sql = (
                    "SELECT id, name, contact, email, address FROM suppliers "
                    "WHERE name LIKE %s OR contact LIKE %s OR email LIKE %s"
                )
                like = f"%{query}%"
                cursor.execute(sql, (like, like, like))
            else:
                cursor.execute(
                    "SELECT id, name, contact, email, address FROM suppliers"
                )
            for row in cursor.fetchall():
                suppliers.append(Supplier.from_row(row))
            conn.close()
        except Exception:
            if conn:
                conn.close()
        return suppliers

    @staticmethod
    def count():
        """Return total number of suppliers."""
        conn = connect_db()
        if not conn:
            return 0
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM suppliers")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except Exception:
            conn.close()
            return 0

    @staticmethod
    def save(mode, name, contact, email, address, supp_id=None):
        """
        Insert or update a supplier.
        Returns (success: bool, message: str).
        """
        conn = connect_db()
        if not conn:
            return False, "Database connection failed."
        try:
            cursor = conn.cursor()
            if mode == "Add":
                cursor.execute(
                    "INSERT INTO suppliers (name, contact, email, address) "
                    "VALUES (%s, %s, %s, %s)",
                    (name, contact, email, address),
                )
            else:
                cursor.execute(
                    "UPDATE suppliers SET name=%s, contact=%s, email=%s, address=%s "
                    "WHERE id=%s",
                    (name, contact, email, address, supp_id),
                )
            conn.commit()
            conn.close()
            return True, f"Supplier record successfully {mode.lower()}ed!"
        except Exception as e:
            conn.close()
            return False, str(e)

    @staticmethod
    def delete(supp_id):
        """Delete supplier by id."""
        conn = connect_db()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM suppliers WHERE id = %s", (supp_id,))
            conn.commit()
            conn.close()
            return True
        except Exception:
            if conn:
                conn.close()
            return False
