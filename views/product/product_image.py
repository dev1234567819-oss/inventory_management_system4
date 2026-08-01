from tkinter import Frame, Label, Button, ttk
from PIL import Image, ImageTk
import os
from utils.messagebox_util import show_error


class ProductImageView:
    def __init__(self, parent, app_controller):
        self.parent = parent
        self.app = app_controller
        self.ctrl = app_controller.product_ctrl

    def render(self):
        content_bg = self.app.get_color("bg_main")
        text_main = self.app.get_color("text_main")
        body = Frame(self.parent, bg=content_bg)
        body.pack(fill="both", expand=True, padx=35, pady=10)

        Label(
            body,
            text="Select a product below to view its associated image:",
            font=("Arial", 10),
            bg=content_bg,
            fg=text_main,
        ).pack(anchor="nw", pady=(0, 10))

        control_frame = Frame(body, bg=content_bg)
        control_frame.pack(fill="x", pady=5)
        Label(
            control_frame,
            text="Choose Product:",
            font=("Arial", 10, "bold"),
            bg=content_bg,
            fg=text_main,
        ).pack(side="left", padx=(0, 10))

        product_names = self.ctrl.get_product_names()

        self.img_combo_var = ttk.Combobox(
            control_frame,
            values=product_names,
            font=("Arial", 10),
            width=25,
            state="readonly",
        )
        if product_names:
            self.img_combo_var.current(0)
        self.img_combo_var.pack(side="left", padx=5)

        Button(
            control_frame,
            text="Show Image",
            bg="#0275d8",
            fg="white",
            font=("Arial", 9, "bold"),
            padx=15,
            pady=5,
            command=self.load_selected_product_image,
        ).pack(side="left", padx=10)

        self.image_display_container = Frame(
            body,
            bg=self.app.get_color("card_bg"),
            bd=1,
            relief="solid",
            width=500,
            height=400,
        )
        self.image_display_container.pack(fill="both", expand=True, pady=15)
        self.image_display_container.pack_propagate(False)

        self.inline_img_label = Label(
            self.image_display_container,
            text="[No Image Loaded. Select a product and click 'Show Image']",
            font=("Arial", 10),
            bg=self.app.get_color("card_bg"),
            fg=text_main,
        )
        self.inline_img_label.pack(expand=True)

    def load_selected_product_image(self):
        selected_prod_name = self.img_combo_var.get()
        if not selected_prod_name:
            show_error(
                "Selection Error", "Please select a product from the dropdown list."
            )
            return

        img_path = self.ctrl.get_image_path(selected_prod_name)
        text_main = self.app.get_color("text_main")
        card_bg = self.app.get_color("card_bg")

        for widget in self.image_display_container.winfo_children():
            widget.destroy()

        if not img_path or img_path == "No Image" or not os.path.exists(img_path):
            Label(
                self.image_display_container,
                text=f"No image file configured or found for '{selected_prod_name}'.",
                font=("Arial", 10, "bold"),
                bg=card_bg,
                fg="#d9534f",
            ).pack(expand=True)
            return

        try:
            pil_img = Image.open(img_path)
            pil_img.thumbnail((420, 350))
            self.current_inline_img = ImageTk.PhotoImage(pil_img)
            Label(
                self.image_display_container,
                text=f"Product: {selected_prod_name}",
                font=("Arial", 11, "bold"),
                bg=card_bg,
                fg=text_main,
            ).pack(pady=(10, 5))
            img_lbl = Label(
                self.image_display_container,
                image=self.current_inline_img,
                bg=card_bg,
            )
            img_lbl.pack(expand=True, pady=5)
        except Exception as e:
            Label(
                self.image_display_container,
                text=f"Error loading image file:\n{e}",
                font=("Arial", 10),
                bg=card_bg,
                fg="red",
            ).pack(expand=True)
