"""Data Access Object for sales."""

from database.db_connection import connect_db
from models.sale import Sale


class SaleDAO:
    @staticmethod
    def get_all():
        """Return list of all Sale records ordered by date descending."""
        conn = connect_db()
        sales = []
        if not conn:
            return sales
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, item_name, selling_price, quantity_sold, total_revenue, sale_date "
                "FROM sales ORDER BY sale_date DESC"
            )
            for row in cursor.fetchall():
                sales.append(Sale.from_row(row))
            conn.close()
        except Exception:
            if conn:
                conn.close()
        return sales

    @staticmethod
    def get_total_revenue():
        """Return sum of total_revenue across all sales."""
        conn = connect_db()
        if not conn:
            return 0.0
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(total_revenue) FROM sales")
            res = cursor.fetchone()[0]
            conn.close()
            return float(res) if res else 0.0
        except Exception:
            if conn:
                conn.close()
            return 0.0

    @staticmethod
    def record_sale(item_name, selling_price, quantity_sold):
        """
        Record a sale and deduct stock.
        Returns (success: bool, result: total_revenue or error message).
        """
        conn = connect_db()
        if not conn:
            return False, "Database connection failed."
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, quantity FROM products WHERE name = %s", (item_name,)
            )
            prod = cursor.fetchone()
            if not prod:
                conn.close()
                return (
                    False,
                    "Item not found in your Product Catalog! Please add it first.",
                )

            prod_id, current_stock = prod[0], prod[1]
            if current_stock < quantity_sold:
                conn.close()
                return (
                    False,
                    f"Insufficient inventory! Current stock available: {current_stock}",
                )

            total_rev = float(selling_price) * int(quantity_sold)
            new_stock = current_stock - quantity_sold

            cursor.execute(
                "INSERT INTO sales (item_name, selling_price, quantity_sold, total_revenue) "
                "VALUES (%s, %s, %s, %s)",
                (item_name, selling_price, quantity_sold, total_rev),
            )

            if new_stock <= 0:
                cursor.execute("DELETE FROM products WHERE id = %s", (prod_id,))
            else:
                cursor.execute(
                    "UPDATE products SET quantity = %s WHERE id = %s",
                    (new_stock, prod_id),
                )

            conn.commit()
            conn.close()
            return True, total_rev
        except Exception as e:
            if conn:
                conn.close()
            return False, str(e)
