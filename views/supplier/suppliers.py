from tkinter import Frame, Button, Label, Entry, Toplevel, ttk
from utils.messagebox_util import show_error, show_info, ask_yes_no


class SuppliersView:
    def __init__(self, parent, app_controller):
        self.parent = parent
        self.app = app_controller
        self.ctrl = app_controller.supplier_ctrl

    def render(self):
        content_bg = self.app.get_color("bg_main")
        body = Frame(self.parent, bg=content_bg)
        body.pack(fill="both", expand=True, padx=35, pady=5)

        toolbar = Frame(body, bg=content_bg)
        toolbar.pack(fill="x", pady=10)

        Button(
            toolbar,
            text="+ Add Supplier",
            bg="#5cb85c",
            fg="white",
            font=("Arial", 9, "bold"),
            padx=10,
            pady=5,
            command=lambda: self.open_supplier_popup("Add"),
        ).pack(side="left", padx=(0, 5))
        Button(
            toolbar,
            text="Edit Supplier",
            bg="#f0ad4e",
            fg="white",
            font=("Arial", 9, "bold"),
            padx=10,
            pady=5,
            command=lambda: self.open_supplier_popup("Edit"),
        ).pack(side="left", padx=5)
        Button(
            toolbar,
            text="Delete Supplier",
            bg="#d9534f",
            fg="white",
            font=("Arial", 9, "bold"),
            padx=10,
            pady=5,
            command=self.delete_supplier,
        ).pack(side="left", padx=5)
        Button(
            toolbar,
            text="Show Purchase History",
            bg="#0275d8",
            fg="white",
            font=("Arial", 9, "bold"),
            padx=10,
            pady=5,
            command=self.show_supplier_purchase_history,
        ).pack(side="left", padx=5)

        search_frame = Frame(toolbar, bg=content_bg)
        search_frame.pack(side="right")
        Label(
            search_frame,
            text="Search Supplier:",
            font=("Arial", 9, "bold"),
            bg=content_bg,
            fg=self.app.get_color("text_main"),
        ).pack(side="left", padx=5)

        self.supp_search_ent = Entry(search_frame, font=("Arial", 10), width=20)
        self.supp_search_ent.pack(side="left", padx=5)
        self.supp_search_ent.bind("<KeyRelease>", self.filter_suppliers)

        columns = (
            "ID",
            "Supplier Name",
            "Contact No",
            "Email Address",
            "Physical Address",
        )
        self.supp_tree = ttk.Treeview(body, columns=columns, show="headings", height=15)
        for col in columns:
            self.supp_tree.heading(col, text=col)
            self.supp_tree.column(col, width=140, anchor="center")
        self.supp_tree.pack(fill="both", expand=True, pady=5)

        self.load_data()

    def load_data(self, search_query=""):
        for item in self.supp_tree.get_children():
            self.supp_tree.delete(item)
        suppliers = self.ctrl.get_suppliers(search_query)
        for s in suppliers:
            self.supp_tree.insert(
                "",
                "end",
                values=(s.id, s.name, s.contact, s.email, s.address),
            )

    def filter_suppliers(self, event):
        query = self.supp_search_ent.get().strip()
        self.load_data(query)

    def delete_supplier(self):
        selected = self.supp_tree.focus()
        if not selected:
            show_error(
                "Error", "Please select a supplier record from the table first."
            )
            return
        values = self.supp_tree.item(selected, "values")
        supp_id = values[0]
        if ask_yes_no(
            "Confirm Deletion",
            "Are you sure you want to permanently delete this supplier?",
        ):
            self.ctrl.delete_supplier(supp_id)
            self.load_data()

    def show_supplier_purchase_history(self):
        selected_item = self.supp_tree.focus()
        if not selected_item:
            show_error(
                "Selection Error",
                "Please select a supplier from the directory table first.",
            )
            return
        values = self.supp_tree.item(selected_item, "values")
        supplier_name = values[1]

        purchase_records = self.ctrl.get_purchase_history(supplier_name)

        history_popup = Toplevel(self.app.root)
        history_popup.title(f"Purchase History: {supplier_name}")
        history_popup.geometry("600x400")
        history_popup.config(bg="white")
        history_popup.grab_set()

        Label(
            history_popup,
            text=f"Purchase History for Supplier: {supplier_name}",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#001f3f",
        ).pack(pady=15)
        table_frame = Frame(history_popup, bg="white")
        table_frame.pack(fill="both", expand=True, padx=20, pady=5)

        columns = ("ID", "Item Name", "Cost Price ($)", "Quantity", "Purchase Date")
        hist_tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", height=12
        )
        for col in columns:
            hist_tree.heading(col, text=col)
            hist_tree.column(col, width=105, anchor="center")
        hist_tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=hist_tree.yview
        )
        scrollbar.pack(side="right", fill="y")
        hist_tree.configure(yscrollcommand=scrollbar.set)

        if purchase_records:
            for p in purchase_records:
                hist_tree.insert(
                    "",
                    "end",
                    values=(
                        p["id"],
                        p["item_name"],
                        f"${p['cost_price']:.2f}",
                        p["quantity"],
                        str(p["purchase_date"])[:19],
                    ),
                )
        else:
            Label(
                history_popup,
                text="No purchase transactions recorded for this supplier.",
                font=("Arial", 10, "italic"),
                bg="white",
                fg="gray",
            ).pack(pady=20)

    def open_supplier_popup(self, mode):
        selected_item = self.supp_tree.focus()
        if mode == "Edit" and not selected_item:
            show_error(
                "Error", "Please select a supplier record from the table to modify."
            )
            return

        popup = Toplevel(self.app.root)
        popup.title(f"{mode} Supplier Record")
        popup.geometry("420x420")
        popup.config(bg="white")
        popup.grab_set()

        Label(
            popup,
            text=f"{mode} Supplier Details",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#001f3f",
        ).pack(pady=15)
        form_frame = Frame(popup, bg="white")
        form_frame.pack(pady=5)

        fields = [
            ("Supplier Name:", "name"),
            ("Contact No:", "contact"),
            ("Email Address:", "email"),
            ("Physical Address:", "address"),
        ]
        entries = {}
        for i, (label_text, key) in enumerate(fields):
            Label(
                form_frame, text=label_text, font=("Arial", 9, "bold"), bg="white"
            ).grid(row=i, column=0, padx=8, pady=8, sticky="e")
            ent = Entry(form_frame, font=("Arial", 10), width=22)
            ent.grid(row=i, column=1, padx=8, pady=8, sticky="w")
            entries[key] = ent

        supp_id = None
        if mode == "Edit":
            values = self.supp_tree.item(selected_item, "values")
            supp_id = values[0]
            entries["name"].insert(0, values[1])
            entries["contact"].insert(0, values[2])
            entries["email"].insert(0, values[3])
            entries["address"].insert(0, values[4])

        def save_action():
            name = entries["name"].get().strip()
            contact = entries["contact"].get().strip()
            email = entries["email"].get().strip()
            address = entries["address"].get().strip()
            success, msg = self.ctrl.save_supplier(
                mode, name, contact, email, address, supp_id
            )
            if success:
                show_info("Success", msg, parent=popup)
                popup.destroy()
                self.load_data()
            else:
                show_error("Database Error", msg, parent=popup)

        Button(
            popup,
            text="Save Record",
            bg="#5cb85c",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18,
            command=save_action,
        ).pack(pady=15)
