from tkinter import Frame, Label, ttk
from services.report_service import ReportService
from dao.sale_dao import SaleDAO


class ProfitLossView:
    def __init__(self, parent, app_controller):
        self.parent = parent
        self.app = app_controller

    def render(self):
        content_bg = self.app.get_color("bg_main")
        body = Frame(self.parent, bg=content_bg)
        body.pack(fill="both", expand=True, padx=35, pady=15)

        Label(
            body,
            text="Annual Profit & Loss Statement",
            font=("Arial", 14, "bold"),
            bg=content_bg,
            fg="#001f3f",
        ).pack(anchor="nw", pady=5)

        total_revenue, total_expenses, net_profit = (
            ReportService.get_profit_loss_summary()
        )

        metrics_frame = Frame(body, bg="white", padx=15, pady=15, relief="solid", bd=1)
        metrics_frame.pack(anchor="nw", pady=5, fill="x")

        Label(
            metrics_frame,
            text=f"Total Revenue (Sales):  ${total_revenue:.2f}",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="green",
        ).grid(row=0, column=0, sticky="w", pady=2)
        Label(
            metrics_frame,
            text=f"Total Expenses (Purchases):  ${total_expenses:.2f}",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="red",
        ).grid(row=1, column=0, sticky="w", pady=2)

        profit_color = "green" if net_profit >= 0 else "red"
        Label(
            metrics_frame,
            text=f"Net Profit / Loss:  ${net_profit:.2f}",
            font=("Arial", 11, "bold"),
            bg="white",
            fg=profit_color,
        ).grid(row=2, column=0, sticky="w", pady=(5, 2))

        Label(
            body,
            text="Revenue Breakdown (Sales Transactions)",
            font=("Arial", 11, "bold"),
            bg=content_bg,
            fg="#001f3f",
        ).pack(anchor="nw", pady=(10, 2))

        rev_frame = Frame(body)
        rev_frame.pack(fill="both", expand=True, pady=2)

        rev_columns = (
            "ID",
            "Item Name",
            "Selling Price ($)",
            "Quantity Sold",
            "Total Revenue ($)",
            "Date & Time",
        )
        rev_tree = ttk.Treeview(
            rev_frame, columns=rev_columns, show="headings", height=5
        )

        rev_scrollbar = ttk.Scrollbar(
            rev_frame, orient="vertical", command=rev_tree.yview
        )
        rev_tree.configure(yscrollcommand=rev_scrollbar.set)

        rev_widths = {
            "ID": 40,
            "Item Name": 140,
            "Selling Price ($)": 100,
            "Quantity Sold": 90,
            "Total Revenue ($)": 110,
            "Date & Time": 150,
        }
        for col in rev_columns:
            rev_tree.heading(col, text=col)
            rev_tree.column(col, width=rev_widths.get(col, 100), anchor="center")

        rev_tree.pack(side="left", fill="both", expand=True)
        rev_scrollbar.pack(side="right", fill="y")

        for s in SaleDAO.get_all():
            rev_tree.insert(
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

        Label(
            body,
            text="Expense Breakdown (Stock Purchases)",
            font=("Arial", 11, "bold"),
            bg=content_bg,
            fg="#001f3f",
        ).pack(anchor="nw", pady=(10, 2))

        exp_frame = Frame(body)
        exp_frame.pack(fill="both", expand=True, pady=2)

        exp_columns = (
            "ID",
            "Item Name",
            "Supplier Name",
            "Cost Price ($)",
            "Quantity",
            "Date & Time",
        )
        exp_tree = ttk.Treeview(
            exp_frame, columns=exp_columns, show="headings", height=5
        )

        exp_scrollbar = ttk.Scrollbar(
            exp_frame, orient="vertical", command=exp_tree.yview
        )
        exp_tree.configure(yscrollcommand=exp_scrollbar.set)

        exp_widths = {
            "ID": 40,
            "Item Name": 140,
            "Supplier Name": 140,
            "Cost Price ($)": 100,
            "Quantity": 80,
            "Date & Time": 150,
        }
        for col in exp_columns:
            exp_tree.heading(col, text=col)
            exp_tree.column(col, width=exp_widths.get(col, 100), anchor="center")

        exp_tree.pack(side="left", fill="both", expand=True)
        exp_scrollbar.pack(side="right", fill="y")

        for p in self.app.purchase_ctrl.get_purchases():
            exp_tree.insert(
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
