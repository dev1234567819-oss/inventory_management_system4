"""Login controller."""

from services.auth_service import AuthService
from utils.messagebox_util import show_error


class LoginController:
    def __init__(self, app_controller):
        self.app = app_controller

    def authenticate(self, username, password):
        if not username or not password:
            show_error("Error", "All fields are required!")
            return
        user = AuthService.login(username, password)
        if user:
            self.app.logged_in_username = user.username
            self.app.show_dashboard_screen(user.username)
        else:
            show_error("Error", "Invalid Username or Password")
