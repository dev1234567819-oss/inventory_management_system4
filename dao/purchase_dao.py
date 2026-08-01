"""Data Access Object for purchases."""

from database.db_connection import connect_db
from models.purchase import Purchase
from dao.product_dao import ProductDAO
import config


class PurchaseDAO:
    @staticmethod
    def get_all():
        """Return list of all Purchase records."""
        conn = connect_db()
        purchases = []
        if not conn:
            return purchases
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, item_name, supplier_name, cost_price, quantity, purchase_date "
                "FROM purchases ORDER BY purchase_date DESC"
            )
            for row in cursor.fetchall():
                purchases.append(Purchase.from_row(row))
            conn.close()
        except Exception:
            if conn:
                conn.close()
        return purchases

    @staticmethod
    def get_by_supplier(supplier_name):
        """Return purchases for a given supplier name (as dicts for history view)."""
        conn = connect_db()
        records = []
        if not conn:
            return records
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT id, item_name, cost_price, quantity, purchase_date "
                "FROM purchases WHERE supplier_name = %s",
                (supplier_name,),
            )
            records = cursor.fetchall()
            conn.close()
        except Exception:
            if conn:
                conn.close()
        return records

    @staticmethod
    def get_total_expenses():
        """Return sum of (cost_price * quantity) across all purchases."""
        conn = connect_db()
        if not conn:
            return 0.0
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(cost_price * quantity) FROM purchases")
            res = cursor.fetchone()[0]
            conn.close()
            return float(res) if res else 0.0
        except Exception:
            if conn:
                conn.close()
            return 0.0

    @staticmethod
    def save(item_name, supplier_name, cost_price, quantity):
        """
        Record a purchase and update product stock.
        Returns (success: bool, sms_triggered: bool or error message).
        """
        conn = connect_db()
        if not conn:
            return False, "Database connection failed."

        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO purchases (item_name, supplier_name, cost_price, quantity) "
                "VALUES (%s, %s, %s, %s)",
                (item_name, supplier_name, cost_price, quantity),
            )

            cursor.execute(
                "SELECT id, quantity FROM products WHERE name = %s", (item_name,)
            )
            prod = cursor.fetchone()

            final_qty = 0
            if prod:
                final_qty = prod[1] + int(quantity)
                cursor.execute(
                    "UPDATE products SET quantity = %s WHERE id = %s",
                    (final_qty, prod[0]),
                )

            conn.commit()
            conn.close()

            sms_triggered = bool(prod and final_qty < config.LOW_STOCK_THRESHOLD)
            return True, sms_triggered
        except Exception as e:
            if conn:
                conn.close()
            return False, str(e)
