"""
Configuration settings for Inventory Management System.
"""

# Database configuration
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Dev@1245789"
DB_NAME = "inventory_management_1_db"
DB_PORT = 3306

# Application settings
APP_TITLE = "Enterprise Inventory & Financial Management System (Advanced)"
APP_GEOMETRY = "1250x750"
APP_MIN_SIZE = (1050, 650)

# Default admin credentials (created on first run)
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "admin123"

# Low stock threshold
LOW_STOCK_THRESHOLD = 5

# Theme colors
THEME_COLORS = {
    "light": {
        "bg_main": "#ffffff",
        "bg_container": "#f4f6f9",
        "bg_sidebar": "#002b66",
        "sidebar_fg": "white",
        "sidebar_active": "#001a40",
        "header_bg": "#001f3f",
        "header_fg": "white",
        "text_main": "#333333",
        "card_bg": "#f8f9fa",
        "card_fg": "#555555",
    },
    "dark": {
        "bg_main": "#1e1e1e",
        "bg_container": "#121212",
        "bg_sidebar": "#2d2d2d",
        "sidebar_fg": "#e0e0e0",
        "sidebar_active": "#3d3d3d",
        "header_bg": "#111111",
        "header_fg": "#ffffff",
        "text_main": "#e0e0e0",
        "card_bg": "#252525",
        "card_fg": "#cccccc",
    },
}
