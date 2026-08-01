"""
Main application controller – owns the root window, theme, navigation,
and wires sub-controllers to views.
"""

from tkinter import Frame, Label, Button, ttk
import config
from database.create_database import create_database_and_tables
from controllers.login_controller import LoginController
from controllers.dashboard_controller import DashboardController
from controllers.product_controller import ProductController
from controllers.supplier_controller import SupplierController
from controllers.purchase_controller import PurchaseController
from controllers.sale_controller import SaleController
from views.login import LoginView
from views.dashboard import DashboardView
from views.product.product_catalog import ProductCatalogView
from views.product.product_image import ProductImageView
from views.supplier.suppliers import SuppliersView
from views.purchase.purchases import PurchasesView
from views.sale.sales import SalesView
from views.report.low_stock import LowStockView
from views.report.profit_loss import ProfitLossView
from views.settings import SettingsView


class InventoryController:
    def __init__(self, root):
        self.root = root
        self.root.title(config.APP_TITLE)
        self.root.geometry(config.APP_GEOMETRY)
        self.root.minsize(*config.APP_MIN_SIZE)

        # Ensure DB/tables exist
        create_database_and_tables()

        self.current_theme = "light"
        self.theme_colors = config.THEME_COLORS
        self.logged_in_username = None

        # Sub-controllers
        self.login_ctrl = LoginController(self)
        self.dashboard_ctrl = DashboardController(self)
        self.product_ctrl = ProductController(self)
        self.supplier_ctrl = SupplierController(self)
        self.purchase_ctrl = PurchaseController(self)
        self.sale_ctrl = SaleController(self)

        self.apply_theme_styles()
        self.show_login_screen()

    def get_color(self, key):
        return self.theme_colors[self.current_theme][key]

    def apply_theme_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        if self.current_theme == "dark":
            style.configure(
                "Treeview",
                background="#252525",
                foreground="#e0e0e0",
                fieldbackground="#252525",
                borderwidth=0,
            )
            style.configure(
                "Treeview.Heading",
                background="#333333",
                foreground="#ffffff",
                relief="flat",
            )
            style.map(
                "Treeview",
                background=[("selected", "#007acc")],
                foreground=[("selected", "#ffffff")],
            )
        else:
            style.configure(
                "Treeview",
                background="#ffffff",
                foreground="#333333",
                fieldbackground="#ffffff",
                borderwidth=1,
            )
            style.configure(
                "Treeview.Heading",
                background="#e1e1e1",
                foreground="#000000",
                relief="raised",
            )
            style.map(
                "Treeview",
                background=[("selected", "#0078d7")],
                foreground=[("selected", "#ffffff")],
            )

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_window()
        LoginView(self.root, self.login_ctrl)

    def show_dashboard_screen(self, logged_in_user):
        self.clear_window()
        self.apply_theme_styles()

        header_bg = self.get_color("header_bg")
        header_fg = self.get_color("header_fg")

        header_frame = Frame(self.root, bg=header_bg, height=55)
        header_frame.pack(side="top", fill="x")
        header_frame.pack_propagate(False)

        Label(
            header_frame,
            text="INVENTORY & FINANCIAL CONTROL SYSTEM",
            bg=header_bg,
            fg=header_fg,
            font=("Arial", 13, "bold"),
        ).pack(side="left", padx=20, pady=12)
        Label(
            header_frame,
            text=f"Logged in as: {logged_in_user} (Administrator)",
            bg=header_bg,
            fg=header_fg,
            font=("Arial", 9),
        ).pack(side="right", padx=20, pady=12)

        container_bg = self.get_color("bg_container")
        container = Frame(self.root, bg=container_bg)
        container.pack(side="top", fill="both", expand=True)

        sidebar_bg = self.get_color("bg_sidebar")
        sidebar_frame = Frame(container, bg=sidebar_bg, width=230)
        sidebar_frame.pack(side="left", fill="y")
        sidebar_frame.pack_propagate(False)

        content_bg = self.get_color("bg_main")
        self.content_area = Frame(container, bg=content_bg)
        self.content_area.pack(side="right", fill="both", expand=True)

        nav_buttons = [
            ("Dashboard", lambda: self.load_content("Dashboard")),
            ("Product Catalog", lambda: self.load_content("Product Catalog")),
            ("Product Image View", lambda: self.load_content("Product Image View")),
            ("Suppliers Directory", lambda: self.load_content("Suppliers Directory")),
            ("Stock Purchases (Cost)", lambda: self.load_content("Stock Purchases")),
            ("Sales History", lambda: self.load_content("Sales History")),
            ("Low Stock Alerts", lambda: self.load_content("Low Stock Alerts")),
            ("Annual Profit & Loss", lambda: self.load_content("Annual Profit & Loss")),
            ("Settings", lambda: self.load_content("Settings")),
        ]

        sidebar_fg = self.get_color("sidebar_fg")
        sidebar_active = self.get_color("sidebar_active")
        for text, command in nav_buttons:
            Button(
                sidebar_frame,
                text=text,
                bg=sidebar_bg,
                fg=sidebar_fg,
                activebackground=sidebar_active,
                activeforeground=sidebar_fg,
                font=("Arial", 10, "bold"),
                bd=0,
                anchor="w",
                padx=20,
                pady=12,
                command=command,
            ).pack(fill="x")

        self.load_content("Dashboard")

    def load_content(self, page_name):
        for widget in self.content_area.winfo_children():
            widget.destroy()
        content_bg = self.get_color("bg_main")
        text_main = self.get_color("text_main")
        self.content_area.config(bg=content_bg)

        if page_name != "Dashboard":
            Label(
                self.content_area,
                text=page_name,
                font=("Arial", 18, "bold"),
                bg=content_bg,
                fg=text_main,
            ).pack(anchor="nw", padx=35, pady=20)

        if page_name == "Dashboard":
            metrics = self.dashboard_ctrl.get_metrics()
            DashboardView(self.content_area, self).render(*metrics)
        elif page_name == "Product Catalog":
            ProductCatalogView(self.content_area, self).render()
        elif page_name == "Product Image View":
            ProductImageView(self.content_area, self).render()
        elif page_name == "Suppliers Directory":
            SuppliersView(self.content_area, self).render()
        elif page_name == "Stock Purchases":
            PurchasesView(self.content_area, self).render()
        elif page_name == "Sales History":
            SalesView(self.content_area, self).render()
        elif page_name == "Low Stock Alerts":
            LowStockView(self.content_area, self).render()
        elif page_name == "Annual Profit & Loss":
            ProfitLossView(self.content_area, self).render()
        elif page_name == "Settings":
            SettingsView(self.content_area, self).render()
