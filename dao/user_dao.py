"""Data Access Object for users."""

from database.db_connection import connect_db
from models.user import User


class UserDAO:
    @staticmethod
    def authenticate(username, password):
        """Return User if credentials match, else None."""
        conn = connect_db()
        if not conn:
            return None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM users WHERE username = %s AND password = %s",
                (username, password),
            )
            row = cursor.fetchone()
            conn.close()
            return User.from_row(row)
        except Exception:
            conn.close()
            return None

    @staticmethod
    def update_password(username, old_password, new_password):
        """
        Update password after verifying old password.
        Returns (success: bool, message: str).
        """
        conn = connect_db()
        if not conn:
            return False, "Database connection failed."
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM users WHERE username = %s AND password = %s",
                (username, old_password),
            )
            user = cursor.fetchone()
            if not user:
                conn.close()
                return False, "Incorrect old password entered."
            cursor.execute(
                "UPDATE users SET password = %s WHERE username = %s",
                (new_password, username),
            )
            conn.commit()
            conn.close()
            return True, "Password changed successfully!"
        except Exception as e:
            conn.close()
            return False, str(e)
