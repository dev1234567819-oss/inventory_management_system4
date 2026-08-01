"""
Inventory Management System – Application entry point.
"""

from tkinter import Tk
from controllers.inventory_controller import InventoryController


if __name__ == "__main__":
    root = Tk()
    app = InventoryController(root)
    root.mainloop()
