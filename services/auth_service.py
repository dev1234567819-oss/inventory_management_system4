"""Authentication and account security service."""

from dao.user_dao import UserDAO


class AuthService:
    @staticmethod
    def login(username, password):
        """Authenticate user. Returns User or None."""
        return UserDAO.authenticate(username, password)

    @staticmethod
    def change_password(username, old_password, new_password):
        """Change password. Returns (success, message)."""
        return UserDAO.update_password(username, old_password, new_password)
