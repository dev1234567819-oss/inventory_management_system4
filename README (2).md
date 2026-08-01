# Inventory Management System

Enterprise Inventory & Financial Management System built with Python (Tkinter) and MySQL.

## Architecture (layered pattern)

```
InventoryManagementSystem/
|-- main.py                  # Application entry point
|-- config.py                # Configuration (DB credentials, themes)
|-- requirements.txt         # Python dependencies
|-- README.md
|
|-- database/
|   |-- db_connection.py     # MySQL connection
|   |-- create_database.py   # Creates DB & tables
|   |-- backup.py            # Database backup utility
|   |-- sql/inventory_db.sql # Schema script
|
|-- models/                  # Domain models
|   |-- user.py, product.py, supplier.py, purchase.py, sale.py
|
|-- dao/                     # Data Access Object layer (SQL only)
|   |-- user_dao.py, product_dao.py, supplier_dao.py,
|   |-- purchase_dao.py, sale_dao.py
|
|-- controllers/             # Connects views with services/DAO
|   |-- inventory_controller.py (main app controller)
|   |-- login_controller.py, dashboard_controller.py,
|   |-- product_controller.py, supplier_controller.py,
|   |-- purchase_controller.py, sale_controller.py
|
|-- views/                   # Tkinter GUI screens
|   |-- login.py, dashboard.py, settings.py
|   |-- product/   (catalog, image view)
|   |-- supplier/  (directory)
|   |-- purchase/  (stock purchases + invoices)
|   |-- sale/      (sales history + invoices)
|   |-- report/    (low stock, profit & loss)
|
|-- services/                # Business logic
|   |-- auth_service.py, validation_service.py,
|   |-- report_service.py, export_service.py
|
|-- utils/                   # Helpers
|   |-- constants.py, helper.py, validator.py, messagebox_util.py
|
|-- assets/                  # Images / icons
|-- reports/                 # Generated PDF / Excel invoices & backups
|-- logs/
|-- tests/
```

## Features (all preserved)

- Secure login (default: `admin` / `admin123`)
- Dashboard with product/supplier counts, revenue, expenses, net profit, SMS-style low-stock alerts
- Product Catalog – add / edit / delete / search, image path, total value
- Product Image View – preview product images
- Suppliers Directory – CRUD + purchase history per supplier
- Stock Purchases – record purchase, update stock, export PDF/Excel invoice
- Sales History – record sale, deduct stock, export PDF/Excel invoice
- Low Stock Alerts – items with quantity &lt; 5, restock request
- Annual Profit & Loss – revenue/expense breakdown tables
- Settings – light/dark theme, change password, logout

## Setup

1. Install MySQL and create a user (or use root).
2. Update credentials in `config.py` if needed.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. (Optional) Create database manually:

```bash
python -m database.create_database
```

   Tables are also auto-created on first app launch.

5. Run:

```bash
python main.py
```

## Default login

- Username: `admin`
- Password: `admin123`
