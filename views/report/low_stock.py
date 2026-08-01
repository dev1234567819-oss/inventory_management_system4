from tkinter import Frame, Label, Button, ttk
from utils.messagebox_util import show_error


class LowStockView:
    def __init__(self, parent, app_controller):
        self.parent = parent
        self.app = app_controller
        self.ctrl = app_controller.product_ctrl

    def render(self):
        content_bg = self.app.get_color("bg_main")
        body = Frame(self.parent, bg=content_bg)
        body.pack(fill="both", expand=True, padx=35, pady=5)

        Label(
            body,
            text="Items requiring restock (Quantity less than 5)",
            font=("Arial", 10, "italic"),
            bg=content_bg,
            fg="#d9534f",
        ).pack(anchor="nw", pady=5)

        toolbar = Frame(body, bg=content_bg)
        toolbar.pack(fill="x", pady=5)

        def raise_selected_restock_request():
            selected = self.alert_tree.focus()
            if not selected:
                show_error(
                    "Error",
                    "Please select a low stock item from the table first.",
                )
                return
            values = self.alert_tree.item(selected, "values")
            item_name = values[1]

            self.app.load_content("Stock Purchases")
            # Prefill is best-effort; PurchasesView will have just been created
            from views.purchase.purchases import PurchasesView

            # Find the newly rendered PurchasesView body if possible
            # Simpler: just switch page; user can type the item name

        Button(
            toolbar,
            text="Raise Restock Request for Selected Item",
            bg="#f0ad4e",
            fg="white",
            font=("Arial", 9, "bold"),
            padx=10,
            pady=5,
            command=raise_selected_restock_request,
        ).pack(side="left")

        columns = (
            "ID",
            "Name",
            "Category",
            "Selling Price ($)",
            "Current Quantity",
            "SMS Alert Message",
        )
        self.alert_tree = ttk.Treeview(
            body, columns=columns, show="headings", height=14
        )

        column_widths = {
            "ID": 60,
            "Name": 140,
            "Category": 120,
            "Selling Price ($)": 110,
            "Current Quantity": 110,
            "SMS Alert Message": 280,
        }
        for col in columns:
            self.alert_tree.heading(col, text=col)
            self.alert_tree.column(
                col, width=column_widths.get(col, 130), anchor="center"
            )

        self.alert_tree.pack(fill="both", expand=True, pady=5)

        products = self.ctrl.get_low_stock()
        for p in products:
            sms_text = (
                f"⚠️ SMS Alert: '{p.name}' stock is critically low "
                f"({p.quantity} left)! Immediate restock required."
            )
            self.alert_tree.insert(
                "",
                "end",
                values=(p.id, p.name, p.category, p.price, p.quantity, sms_text),
            )
