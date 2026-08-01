from tkinter import Frame, Label, Text, Scrollbar


class DashboardView:
    def __init__(self, parent, app_controller):
        self.parent = parent
        self.controller = app_controller

    def render(
        self, prod_count, supp_count, low_stock_items, total_revenue, total_expenses
    ):
        content_bg = self.controller.get_color("bg_main")
        text_main = self.controller.get_color("text_main")

        body = Frame(self.parent, bg=content_bg)
        body.pack(fill="both", expand=True, padx=35, pady=15)

        Label(
            body,
            text="Dashboard Analytics",
            font=("Arial", 16, "bold"),
            bg=content_bg,
            fg=text_main,
        ).pack(anchor="nw", pady=(0, 10))

        metrics_grid = Frame(body, bg=content_bg)
        metrics_grid.pack(fill="x", pady=5)

        def create_colored_metric_card(parent, title, value, row, col, bg_card_color):
            card = Frame(
                parent,
                bg=bg_card_color,
                bd=1,
                relief="solid",
                padx=15,
                pady=12,
                width=220,
                height=80,
            )
            card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
            card.pack_propagate(False)
            Label(
                card,
                text=title,
                font=("Arial", 9, "bold"),
                bg=bg_card_color,
                fg="white",
            ).pack(anchor="center")
            Label(
                card,
                text=str(value),
                font=("Arial", 16, "bold"),
                bg=bg_card_color,
                fg="white",
            ).pack(anchor="center", pady=(5, 0))

        net_profit = total_revenue - total_expenses
        net_box_color = "#16a085" if net_profit >= 0 else "#e74c3c"

        create_colored_metric_card(
            metrics_grid, "Total Products", prod_count, 0, 0, "#2980b9"
        )
        create_colored_metric_card(
            metrics_grid, "Total Suppliers", supp_count, 0, 1, "#8e44ad"
        )
        create_colored_metric_card(
            metrics_grid,
            "Raised Purchase Requests",
            len(low_stock_items),
            0,
            2,
            "#d35400",
        )
        create_colored_metric_card(
            metrics_grid,
            "Annual Revenue",
            f"${total_revenue:,.2f}",
            1,
            0,
            "#27ae60",
        )
        create_colored_metric_card(
            metrics_grid,
            "Annual Expenses",
            f"${total_expenses:,.2f}",
            1,
            1,
            "#c0392b",
        )
        create_colored_metric_card(
            metrics_grid,
            "Annual Net Profit",
            f"${net_profit:,.2f}",
            1,
            2,
            net_box_color,
        )

        metrics_grid.columnconfigure(0, weight=1)
        metrics_grid.columnconfigure(1, weight=1)
        metrics_grid.columnconfigure(2, weight=1)

        sms_outer_frame = Frame(body, bg=content_bg, bd=1, relief="solid")
        sms_outer_frame.pack(fill="both", expand=True, pady=(15, 5))

        sms_title_frame = Frame(
            sms_outer_frame, bg=self.controller.get_color("card_bg"), height=30
        )
        sms_title_frame.pack(fill="x", side="top")
        sms_title_frame.pack_propagate(False)
        Label(
            sms_title_frame,
            text="SMS Notification Alert Box",
            font=("Arial", 9, "bold"),
            bg=self.controller.get_color("card_bg"),
            fg=text_main,
        ).pack(side="left", padx=10, pady=5)

        text_container = Frame(sms_outer_frame, bg=content_bg)
        text_container.pack(fill="both", expand=True, padx=5, pady=5)

        sms_scroll = Scrollbar(text_container)
        sms_scroll.pack(side="right", fill="y")

        sms_text_box = Text(
            text_container,
            font=("Consolas", 10),
            bg=content_bg,
            fg=text_main,
            bd=0,
            yscrollcommand=sms_scroll.set,
            wrap="word",
            height=12,
        )
        sms_text_box.pack(side="left", fill="both", expand=True)
        sms_scroll.config(command=sms_text_box.yview)

        if low_stock_items:
            sms_text_box.insert(
                "end", "[SMS Notification] Low Stock Purchase Requests Raised:\n\n"
            )
            for item_name, qty in low_stock_items:
                sms_text_box.insert(
                    "end",
                    f"ALERT: Product '{item_name}' has fallen to {qty} units. "
                    "Restock request sent to suppliers.\n",
                )
        else:
            sms_text_box.insert(
                "end",
                "[SMS Inbox Empty] No low stock purchase request messages generated yet.\n",
            )
        sms_text_box.config(state="disabled")
