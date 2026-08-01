"""Data Access Object for products."""

from database.db_connection import connect_db
from models.product import Product
import config


class ProductDAO:
    @staticmethod
    def get_all(query=""):
        """Return list of Product objects, optionally filtered by search query."""
        conn = connect_db()
        products = []
        if not conn:
            return products
        try:
            cursor = conn.cursor()
            if query:
                sql = (
                    "SELECT id, name, brand, category, price, quantity, image_path "
                    "FROM products WHERE name LIKE %s OR brand LIKE %s OR category LIKE %s"
                )
                like = f"%{query}%"
                cursor.execute(sql, (like, like, like))
            else:
                cursor.execute(
                    "SELECT id, name, brand, category, price, quantity, image_path FROM products"
                )
            for row in cursor.fetchall():
                products.append(Product.from_row(row))
            conn.close()
        except Exception:
            if conn:
                conn.close()
        return products

    @staticmethod
    def get_by_name(name):
        """Return Product by name or None."""
        conn = connect_db()
        if not conn:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, brand, category, price, quantity, image_path "
                "FROM products WHERE name = %s",
                (name,),
            )
            row = cursor.fetchone()
            conn.close()
            return Product.from_row(row) if row else None
        except Exception:
            conn.close()
            return None

    @staticmethod
    def get_product_names():
        """Return list of product names."""
        conn = connect_db()
        names = []
        if not conn:
            return names
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM products")
            names = [row[0] for row in cursor.fetchall()]
            conn.close()
        except Exception:
            if conn:
                conn.close()
        return names

    @staticmethod
    def get_image_path(product_name):
        """Return image_path for a product name."""
        conn = connect_db()
        if not conn:
            return None
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT image_path FROM products WHERE name = %s", (product_name,)
            )
            res = cursor.fetchone()
            conn.close()
            return res[0] if res else None
        except Exception:
            conn.close()
            return None

    @staticmethod
    def get_low_stock(threshold=None):
        """Return list of products with quantity below threshold."""
        if threshold is None:
            threshold = config.LOW_STOCK_THRESHOLD
        conn = connect_db()
        products = []
        if not conn:
            return products
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, brand, category, price, quantity, image_path "
                "FROM products WHERE quantity < %s",
                (threshold,),
            )
            for row in cursor.fetchall():
                products.append(Product.from_row(row))
            conn.close()
        except Exception:
            if conn:
                conn.close()
        return products

    @staticmethod
    def count():
        """Return total number of products."""
        conn = connect_db()
        if not conn:
            return 0
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM products")
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except Exception:
            conn.close()
            return 0

    @staticmethod
    def save(mode, name, brand, category, price, quantity, image_path, prod_id=None):
        """
        Insert or update a product.
        mode: 'Add' or 'Edit'
        Returns (success: bool, message: str).
        """
        conn = connect_db()
        if not conn:
            return False, "Database connection failed."
        try:
            cursor = conn.cursor()
            if mode == "Add":
                cursor.execute(
                    "INSERT INTO products (name, brand, category, price, quantity, image_path) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (name, brand, category, price, quantity, image_path),
                )
            else:
                cursor.execute(
                    "UPDATE products SET name=%s, brand=%s, category=%s, price=%s, "
                    "quantity=%s, image_path=%s WHERE id=%s",
                    (name, brand, category, price, quantity, image_path, prod_id),
                )
            conn.commit()
            conn.close()
            return True, f"Product record successfully {mode.lower()}ed!"
        except Exception as e:
            conn.close()
            return False, str(e)

    @staticmethod
    def delete(prod_id):
        """Delete product by id."""
        conn = connect_db()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id = %s", (prod_id,))
            conn.commit()
            conn.close()
            return True
        except Exception:
            if conn:
                conn.close()
            return False

    @staticmethod
    def update_quantity(prod_id, new_quantity):
        """Update product quantity. If <= 0, delete the product."""
        conn = connect_db()
        if not conn:
            return False
        try:
            cursor = conn.cursor()
            if new_quantity <= 0:
                cursor.execute("DELETE FROM products WHERE id = %s", (prod_id,))
            else:
                cursor.execute(
                    "UPDATE products SET quantity = %s WHERE id = %s",
                    (new_quantity, prod_id),
                )
            conn.commit()
            conn.close()
            return True
        except Exception:
            if conn:
                conn.close()
            return False
