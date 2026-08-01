from tkinter import Frame, Label, Entry, Button, ttk, filedialog
from utils.messagebox_util import show_error, show_info


class SalesView:
    def __init__(self, parent, app_controller):
        self.parent = parent
        self.app = app_controller
        self.ctrl = app_controller.sale_ctrl

    def render(self):
        content_bg = self.app.get_color("bg_main")
        body = Frame(self.parent, bg=content_bg)
        body.pack(fill="both", expand=True, padx=35, pady=15)

        Label(
            body,
            text="Sales History & Invoicing",
            font=("Arial", 14, "bold"),
            bg=content_bg,
            fg="#001f3f",
        ).pack(anchor="nw", pady=5)

        form_frame = Frame(body, bg="white", padx=15, pady=15, relief="solid", bd=1)
        form_frame.pack(anchor="nw", pady=5, fill="x")

        Label(
            form_frame,
            text="Record New Sale & Generate Invoice",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#001f3f",
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        fields = [
            ("Item Name:", "item"),
            ("Selling Price ($):", "price"),
            ("Quantity Sold:", "qty"),
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
            for item in self.sales_tree.get_children():
                self.sales_tree.delete(item)
            for s in self.ctrl.get_sales():
                self.sales_tree.insert(
                    "",
                    "end",
                    values=(
                        s.id,
                        s.item_name,
                        s.selling_price,
                        s.quantity_sold,
                        s.total_revenue,
                        s.sale_date,
                    ),
                )

        def process_sale_and_export(export_type):
            item = self.entries["item"].get().strip()
            price_str = self.entries["price"].get().strip()
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

            success, result = self.ctrl.process_sale(
                item, price_str, qty_str, export_type, file_path or None
            )
            if not success:
                show_error("Error", result)
                return

            if file_path:
                show_info(
                    "Success",
                    f"Sale recorded & stock updated!\nSaved to PC at:\n{file_path}",
                )
            else:
                show_info("Success", "Sale recorded & stock updated!")

            clear_form()
            update_table()

        btn_frame = Frame(form_frame, bg="white")
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

        Button(
            btn_frame,
            text="Save & View PDF Invoice",
            bg="#d9534f",
            fg="white",
            font=("Arial", 9, "bold"),
            padx=8,
            pady=5,
            command=lambda: process_sale_and_export("pdf"),
        ).pack(side="left", padx=5)
        Button(
            btn_frame,
            text="Save & View Excel Invoice",
            bg="#5cb85c",
            fg="white",
            font=("Arial", 9, "bold"),
            padx=8,
            pady=5,
            command=lambda: process_sale_and_export("excel"),
        ).pack(side="left", padx=5)

        Label(
            body,
            text="Previous Sales Transactions History",
            font=("Arial", 11, "bold"),
            bg=content_bg,
            fg="#001f3f",
        ).pack(anchor="nw", pady=(15, 5))

        table_frame = Frame(body)
        table_frame.pack(fill="both", expand=True, pady=5)

        columns = (
            "ID",
            "Item Name",
            "Selling Price ($)",
            "Quantity Sold",
            "Total Revenue ($)",
            "Date & Time",
        )
        self.sales_tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", height=8
        )

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.sales_tree.yview
        )
        self.sales_tree.configure(yscrollcommand=scrollbar.set)

        column_widths = {
            "ID": 50,
            "Item Name": 150,
            "Selling Price ($)": 110,
            "Quantity Sold": 100,
            "Total Revenue ($)": 130,
            "Date & Time": 180,
        }
        for col in columns:
            self.sales_tree.heading(col, text=col)
            self.sales_tree.column(
                col, width=column_widths.get(col, 120), anchor="center"
            )

        self.sales_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        update_table()
