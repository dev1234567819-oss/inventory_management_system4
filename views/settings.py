from tkinter import Frame, Label, Button, Toplevel, Entry, Canvas, Scrollbar
from services.auth_service import AuthService
from services.validation_service import ValidationService
from utils.messagebox_util import show_error, show_info


class SettingsView:
    def __init__(self, parent, app_controller):
        self.parent = parent
        self.controller = app_controller

    def render(self):
        content_bg = self.controller.get_color("bg_main")
        text_main = self.controller.get_color("text_main")
        card_bg = self.controller.get_color("card_bg")

        outer_frame = Frame(self.parent, bg=content_bg)
        outer_frame.pack(fill="both", expand=True, padx=35, pady=20)

        Label(
            outer_frame,
            text="System Preferences & Controls",
            font=("Arial", 14, "bold"),
            bg=content_bg,
            fg=text_main,
        ).pack(anchor="nw", pady=(0, 15))

        container_frame = Frame(outer_frame, bg=content_bg)
        container_frame.pack(fill="both", expand=True)

        canvas = Canvas(container_frame, bg=content_bg, highlightthickness=0)
        scrollbar = Scrollbar(container_frame, orient="vertical", command=canvas.yview)

        scrollable_content = Frame(canvas, bg=content_bg)

        scrollable_content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )

        canvas_window = canvas.create_window(
            (0, 0), window=scrollable_content, anchor="nw"
        )

        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)

        canvas.bind("<Configure>", on_canvas_configure)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Theme card
        theme_card = Frame(
            scrollable_content, bg=card_bg, bd=1, relief="solid", padx=20, pady=20
        )
        theme_card.pack(fill="x", pady=10)
        Label(
            theme_card,
            text="Appearance Theme",
            font=("Arial", 11, "bold"),
            bg=card_bg,
            fg=text_main,
        ).pack(anchor="nw", pady=(0, 5))
        Label(
            theme_card,
            text=f"Current Theme: {self.controller.current_theme.capitalize()} Mode",
            font=("Arial", 9),
            bg=card_bg,
            fg=text_main,
        ).pack(anchor="nw", pady=(0, 15))

        def toggle_theme():
            self.controller.current_theme = (
                "dark" if self.controller.current_theme == "light" else "light"
            )
            self.controller.show_dashboard_screen(
                getattr(self.controller, "logged_in_username", "admin")
            )
            self.controller.load_content("Settings")

        theme_btn_text = (
            "Switch to Dark Theme"
            if self.controller.current_theme == "light"
            else "Switch to Light Theme"
        )
        Button(
            theme_card,
            text=theme_btn_text,
            bg="#0275d8",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            command=toggle_theme,
        ).pack(anchor="nw")

        # Security card
        security_card = Frame(
            scrollable_content, bg=card_bg, bd=1, relief="solid", padx=20, pady=20
        )
        security_card.pack(fill="x", pady=10)
        Label(
            security_card,
            text="Account Security",
            font=("Arial", 11, "bold"),
            bg=card_bg,
            fg=text_main,
        ).pack(anchor="nw", pady=(0, 5))
        Label(
            security_card,
            text="Update your account login password securely by verifying your old password.",
            font=("Arial", 9),
            bg=card_bg,
            fg=text_main,
        ).pack(anchor="nw", pady=(0, 15))
        Button(
            security_card,
            text="Change Password",
            bg="#f0ad4e",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            command=self.open_change_password_popup,
        ).pack(anchor="nw")

        # Session card
        account_card = Frame(
            scrollable_content, bg=card_bg, bd=1, relief="solid", padx=20, pady=20
        )
        account_card.pack(fill="x", pady=10)
        Label(
            account_card,
            text="Session Management",
            font=("Arial", 11, "bold"),
            bg=card_bg,
            fg=text_main,
        ).pack(anchor="nw", pady=(0, 5))
        Label(
            account_card,
            text="Sign out of your active administrative session securely.",
            font=("Arial", 9),
            bg=card_bg,
            fg=text_main,
        ).pack(anchor="nw", pady=(0, 15))
        Button(
            account_card,
            text="Logout from System",
            bg="#c9302c",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            command=self.controller.show_login_screen,
        ).pack(anchor="nw")

    def open_change_password_popup(self):
        popup = Toplevel(self.controller.root)
        popup.title("Change Password")
        popup.geometry("380x300")
        popup.config(bg="white")
        popup.grab_set()

        Label(
            popup,
            text="Change Account Password",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#001f3f",
        ).pack(pady=15)
        form_frame = Frame(popup, bg="white")
        form_frame.pack(pady=5)

        fields = [
            ("Old Password:", "old_pass"),
            ("New Password:", "new_pass"),
            ("Confirm New Password:", "confirm_pass"),
        ]
        entries = {}
        for i, (label_text, key) in enumerate(fields):
            Label(
                form_frame, text=label_text, font=("Arial", 9, "bold"), bg="white"
            ).grid(row=i, column=0, padx=8, pady=8, sticky="e")
            ent = Entry(form_frame, font=("Arial", 10), width=18, show="*")
            ent.grid(row=i, column=1, padx=8, pady=8, sticky="w")
            entries[key] = ent

        def save_new_password():
            old_p = entries["old_pass"].get().strip()
            new_p = entries["new_pass"].get().strip()
            confirm_p = entries["confirm_pass"].get().strip()

            ok, msg = ValidationService.validate_password_change(
                old_p, new_p, confirm_p
            )
            if not ok:
                show_error("Error", msg, parent=popup)
                return

            current_user = getattr(self.controller, "logged_in_username", "admin")
            success, msg = AuthService.change_password(current_user, old_p, new_p)
            if success:
                show_info("Success", msg, parent=popup)
                popup.destroy()
            else:
                show_error("Error", msg, parent=popup)

        Button(
            popup,
            text="Update Password",
            bg="#0275d8",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18,
            command=save_new_password,
        ).pack(pady=15)
