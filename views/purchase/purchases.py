from tkinter import Frame, Label, Entry, Button, ttk, filedialog
from utils.messagebox_util import show_error, show_info, show_warning


class PurchasesView:
    def __init__(self, parent, app_controller):
        self.parent = parent
        self.app = app_controller
        self.ctrl = app_controller.purchase_ctrl

    def render(self):
        content_bg = self.app.get_color("bg_main")
        body = Frame(self.parent, bg=content_bg)
        body.pack(fill="both", expand=True, padx=35, pady=15)

        Label(
            body,
            text="Stock Purchases & Supplier Invoicing",
            font=("Arial", 14, "bold"),
            bg=content_bg,
            fg="#001f3f",
        ).pack(anchor="nw", pady=5)

        form_frame = Frame(body, bg="white", padx=15, pady=15, relief="solid", bd=1)
        form_frame.pack(anchor="nw", pady=5, fill="x")

        Label(
            form_frame,
            text="Record New Purchase & Generate Invoices",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#001f3f",
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        fields = [
            ("Item Name:", "item"),
            ("Supplier Name:", "supplier"),
            ("Cost Price ($):", "cost"),
            ("Quantity Purchased:", "qty"),
        ]
        self.entries = {}
        for i, (label_text, key) in enumerate(fields, start=1):
            Label(
                form_frame, text=label_text, font=("Arial", 9, "bold"), bg="white"
            ).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            ent = Entry(form_frame, font=("Arial", 9), width=25)
            ent.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            self.entries[key] = ent

        def clear_form():
            for ent in self.entries.values():
                ent.delete(0, "end")

        def update_table():
            for item in self.purchases_tree.get_children():
                self.purchases_tree.delete(item)
            for p in self.ctrl.get_purchases():
                self.purchases_tree.insert(
                    "",
                    "end",
                    values=(
                        p.id,
                        p.item_name,
                        p.supplier_name,
                        p.cost_price,
                        p.quantity,
                        p.purchase_date,
                    ),
                )

        def process_purchase_and_export(export_type):
            item = self.entries["item"].get().strip()
            supplier = self.entries["supplier"].get().strip()
            cost_str = self.entries["cost"].get().strip()
            qty_str = self.entries["qty"].get().strip()

            default_name = self.ctrl.default_invoice_name(item or "item")
            file_path = ""
            if export_type == "pdf":
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".pdf",
                    filetypes=[("PDF files", "*.pdf")],
                    initialfile=default_name,
                )
            elif export_type == "excel":
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".xlsx",
                    filetypes=[("Excel files", "*.xlsx")],
                    initialfile=default_name,
                )

            if not file_path and export_type in ("pdf", "excel"):
                # User cancelled save dialog – still allow record without export
                pass

            success, result = self.ctrl.process_purchase(
                item, supplier, cost_str, qty_str, export_type, file_path or None
            )
            if not success:
                show_error("Error", result)
                return

            if file_path:
                show_info(
                    "Success",
                    f"Purchase recorded & inventory updated!\nSaved to PC at:\n{file_path}",
                )
            else:
                show_info("Success", "Purchase recorded & inventory updated!")

            if result.get("sms_triggered"):
                show_warning(
                    "Low Stock Warning",
                    f"Warning: Stock for '{item}' is below 5 units after this operation!",
                )

            clear_form()
            update_table()

        btn_frame = Frame(form_frame, bg="white")
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)

        Button(
            btn_frame,
            text="Save & View PDF Invoice",
            bg="#d9534f",
            fg="white",
            font=("Arial", 9, "bold"),
            padx=8,
            pady=5,
            command=lambda: process_purchase_and_export("pdf"),
        ).pack(side="left", padx=5)
        Button(
            btn_frame,
            text="Save & View Excel Invoice",
            bg="#5cb85c",
            fg="white",
            font=("Arial", 9, "bold"),
            padx=8,
            pady=5,
            command=lambda: process_purchase_and_export("excel"),
        ).pack(side="left", padx=5)

        Label(
            body,
            text="Previous Purchase Transactions History",
            font=("Arial", 11, "bold"),
            bg=content_bg,
            fg="#001f3f",
        ).pack(anchor="nw", pady=(15, 5))

        table_frame = Frame(body)
        table_frame.pack(fill="both", expand=True, pady=5)

        columns = (
            "ID",
            "Item Name",
            "Supplier Name",
            "Cost Price ($)",
            "Quantity",
            "Date & Time",
        )
        self.purchases_tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", height=8
        )

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.purchases_tree.yview
        )
        self.purchases_tree.configure(yscrollcommand=scrollbar.set)

        column_widths = {
            "ID": 50,
            "Item Name": 150,
            "Supplier Name": 150,
            "Cost Price ($)": 110,
            "Quantity": 100,
            "Date & Time": 180,
        }
        for col in columns:
            self.purchases_tree.heading(col, text=col)
            self.purchases_tree.column(
                col, width=column_widths.get(col, 120), anchor="center"
            )

        self.purchases_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        update_table()

    def open_purchase_popup(self, prefill_item=None, prefill_qty=None):
        """Called from Low Stock view to prefill restock request."""
        if prefill_item and "item" in getattr(self, "entries", {}):
            self.entries["item"].delete(0, "end")
            self.entries["item"].insert(0, prefill_item)
        if prefill_qty and "qty" in getattr(self, "entries", {}):
            self.entries["qty"].delete(0, "end")
            self.entries["qty"].insert(0, prefill_qty)
