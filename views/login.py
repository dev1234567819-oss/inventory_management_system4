from tkinter import Frame, Label, Button, ttk


class LoginView:
    def __init__(self, root, login_controller):
        self.root = root
        self.controller = login_controller
        self.render()

    def render(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        login_frame = Frame(self.root, bg="#001f3f")
        login_frame.pack(fill="both", expand=True)

        card = Frame(login_frame, bg="white", padx=50, pady=40, relief="raised", bd=2)
        card.place(relx=0.5, rely=0.5, anchor="center")

        Label(
            card,
            text="INVENTORY LOGIN",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#001f3f",
        ).pack(pady=(0, 20))
        Label(
            card, text="Username", font=("Arial", 10, "bold"), bg="white", anchor="w"
        ).pack(anchor="w")

        self.username_entry = ttk.Entry(card, font=("Arial", 12), width=28)
        self.username_entry.pack(pady=(5, 15))

        Label(
            card, text="Password", font=("Arial", 10, "bold"), bg="white", anchor="w"
        ).pack(anchor="w")
        self.password_entry = ttk.Entry(card, font=("Arial", 12), width=28, show="*")
        self.password_entry.pack(pady=(5, 20))

        Button(
            card,
            text="Secure Login",
            bg="#001f3f",
            fg="white",
            font=("Arial", 10, "bold"),
            width=22,
            command=self.handle_login,
        ).pack(pady=5)

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        self.controller.authenticate(username, password)
