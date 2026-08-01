from tkinter import Frame, Button, Label, Entry, Toplevel, ttk, filedialog
from utils.messagebox_util import show_error, show_info, ask_yes_no


class ProductCatalogView:
    def __init__(self, parent, app_controller):
        self.parent = parent
        self.app = app_controller
        self.ctrl = app_controller.product_ctrl

    def render(self):
        content_bg = self.app.get_color("bg_main")
        body = Frame(self.parent, bg=content_bg)
        body.pack(fill="both", expand=True, padx=35, pady=5)

        toolbar = Frame(body, bg=content_bg)
        toolbar.pack(fill="x", pady=10)

        Button(
            toolbar,
            text="+ Add Product",
            bg="#5cb85c",
            fg="white",
            font=("Arial", 9, "bold"),
            padx=10,
            pady=5,
            command=lambda: self.open_product_popup("Add"),
        ).pack(side="left", padx=(0, 5))
        Button(
            toolbar,
            text="Edit Product",
            bg="#f0ad4e",
            fg="white",
            font=("Arial", 9, "bold"),
            padx=10,
            pady=5,
            command=lambda: self.open_product_popup("Edit"),
        ).pack(side="left", padx=5)
        Button(
            toolbar,
            text="Delete Product",
            bg="#d9534f",
            fg="white",
            font=("Arial", 9, "bold"),
            padx=10,
            pady=5,
            command=self.delete_product,
        ).pack(side="left", padx=5)

        search_frame = Frame(toolbar, bg=content_bg)
        search_frame.pack(side="right")
        Label(
            search_frame,
            text="Search Product:",
            font=("Arial", 9, "bold"),
            bg=content_bg,
            fg=self.app.get_color("text_main"),
        ).pack(side="left", padx=5)

        self.prod_search_ent = Entry(search_frame, font=("Arial", 10), width=20)
        self.prod_search_ent.pack(side="left", padx=5)
        self.prod_search_ent.bind("<KeyRelease>", self.filter_products)

        columns = (
            "ID",
            "Name",
            "Brand",
            "Category",
            "Selling Price ($)",
            "Quantity",
            "Total Value ($)",
            "Image Path",
        )
        self.prod_tree = ttk.Treeview(body, columns=columns, show="headings", height=14)
        for col in columns:
            self.prod_tree.heading(col, text=col)
            self.prod_tree.column(col, width=110, anchor="center")
        self.prod_tree.pack(fill="both", expand=True, pady=5)

        self.load_data()

    def load_data(self, search_query=""):
        for item in self.prod_tree.get_children():
            self.prod_tree.delete(item)
        products = self.ctrl.get_products(search_query)
        for p in products:
            brand_str = p.brand if p.brand else "N/A"
            img_str = p.image_path if p.image_path else "No Image"
            self.prod_tree.insert(
                "",
                "end",
                values=(
                    p.id,
                    p.name,
                    brand_str,
                    p.category,
                    f"{p.price:.2f}",
                    p.quantity,
                    f"{p.total_value:.2f}",
                    img_str,
                ),
            )

    def filter_products(self, event):
        query = self.prod_search_ent.get().strip()
        self.load_data(query)

    def delete_product(self):
        selected = self.prod_tree.focus()
        if not selected:
            show_error("Error", "Please select a product record from the table first.")
            return
        values = self.prod_tree.item(selected, "values")
        prod_id = values[0]
        if ask_yes_no(
            "Confirm Deletion",
            "Are you sure you want to permanently delete this product?",
        ):
            self.ctrl.delete_product(prod_id)
            self.load_data()

    def open_product_popup(self, mode):
        selected_item = self.prod_tree.focus()
        if mode == "Edit" and not selected_item:
            show_error(
                "Error", "Please select a product record from the table to modify."
            )
            return

        popup = Toplevel(self.app.root)
        popup.title(f"{mode} Product Record")
        popup.geometry("480x500")
        popup.config(bg="white")
        popup.grab_set()

        Label(
            popup,
            text=f"{mode} Product Details",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#001f3f",
        ).pack(pady=15)
        form_frame = Frame(popup, bg="white")
        form_frame.pack(pady=5)

        Label(
            form_frame, text="Product Name:", font=("Arial", 9, "bold"), bg="white"
        ).grid(row=0, column=0, padx=8, pady=8, sticky="e")
        name_ent = Entry(form_frame, font=("Arial", 10), width=22)
        name_ent.grid(row=0, column=1, padx=8, pady=8, sticky="w")

        Label(
            form_frame, text="Brand Name:", font=("Arial", 9, "bold"), bg="white"
        ).grid(row=1, column=0, padx=8, pady=8, sticky="e")
        brand_ent = Entry(form_frame, font=("Arial", 10), width=22)
        brand_ent.grid(row=1, column=1, padx=8, pady=8, sticky="w")

        Label(
            form_frame, text="Category:", font=("Arial", 9, "bold"), bg="white"
        ).grid(row=2, column=0, padx=8, pady=8, sticky="e")
        cat_ent = Entry(form_frame, font=("Arial", 10), width=22)
        cat_ent.grid(row=2, column=1, padx=8, pady=8, sticky="w")

        Label(
            form_frame, text="Selling Price ($):", font=("Arial", 9, "bold"), bg="white"
        ).grid(row=3, column=0, padx=8, pady=8, sticky="e")
        price_ent = Entry(form_frame, font=("Arial", 10), width=22)
        price_ent.grid(row=3, column=1, padx=8, pady=8, sticky="w")

        Label(
            form_frame, text="Initial Quantity:", font=("Arial", 9, "bold"), bg="white"
        ).grid(row=4, column=0, padx=8, pady=8, sticky="e")
        qty_ent = Entry(form_frame, font=("Arial", 10), width=22)
        qty_ent.grid(row=4, column=1, padx=8, pady=8, sticky="w")

        Label(
            form_frame, text="Image File Path:", font=("Arial", 9, "bold"), bg="white"
        ).grid(row=5, column=0, padx=8, pady=8, sticky="e")
        img_ent = Entry(form_frame, font=("Arial", 10), width=22)
        img_ent.grid(row=5, column=1, padx=8, pady=8, sticky="w")

        def browse_image():
            file_path = filedialog.askopenfilename(
                title="Select Product Image",
                filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp")],
            )
            if file_path:
                img_ent.delete(0, "end")
                img_ent.insert(0, file_path)

        Button(
            form_frame,
            text="Browse...",
            bg="#0275d8",
            fg="white",
            font=("Arial", 8, "bold"),
            command=browse_image,
        ).grid(row=5, column=2, padx=5, sticky="w")

        prod_id = None
        if mode == "Edit":
            values = self.prod_tree.item(selected_item, "values")
            prod_id = values[0]
            name_ent.insert(0, values[1])
            if values[2] != "N/A":
                brand_ent.insert(0, values[2])
            cat_ent.insert(0, values[3])
            price_ent.insert(0, values[4])
            qty_ent.insert(0, values[5])
            if values[7] != "No Image":
                img_ent.insert(0, values[7])

        def save_action():
            name = name_ent.get().strip()
            brand = brand_ent.get().strip()
            cat = cat_ent.get().strip()
            price = price_ent.get().strip()
            qty = qty_ent.get().strip()
            img_path = img_ent.get().strip()

            success, msg = self.ctrl.save_product(
                mode, name, brand, cat, price, qty, img_path, prod_id
            )
            if success:
                show_info("Success", msg, parent=popup)
                popup.destroy()
                self.load_data()
            else:
                show_error("Error", msg, parent=popup)

        Button(
            popup,
            text="Save Record",
            bg="#5cb85c",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18,
            command=save_action,
        ).pack(pady=15)
