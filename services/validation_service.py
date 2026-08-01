"""Validation service for forms."""

from utils.validator import is_non_empty, is_valid_float, is_valid_int


class ValidationService:
    @staticmethod
    def validate_product(name, price, quantity):
        if not is_non_empty(name, price, quantity):
            return False, "Name, Price, and Quantity fields cannot be empty."
        if not is_valid_float(price):
            return False, "Price must be a valid number."
        if not is_valid_int(quantity):
            return False, "Quantity must be an integer."
        return True, ""

    @staticmethod
    def validate_supplier(name):
        if not is_non_empty(name):
            return False, "Supplier Name field is required."
        return True, ""

    @staticmethod
    def validate_purchase(item, supplier, cost, qty):
        if not is_non_empty(item, supplier, cost, qty):
            return False, "All fields are required."
        if not is_valid_float(cost):
            return False, "Cost price must be a number."
        if not is_valid_int(qty):
            return False, "Quantity must be an integer."
        return True, ""

    @staticmethod
    def validate_sale(item, price, qty):
        if not is_non_empty(item, price, qty):
            return False, "All fields are required."
        if not is_valid_float(price):
            return False, "Selling price must be a number."
        if not is_valid_int(qty):
            return False, "Quantity must be an integer."
        return True, ""

    @staticmethod
    def validate_password_change(old_p, new_p, confirm_p):
        if not is_non_empty(old_p, new_p, confirm_p):
            return False, "All password fields are required."
        if new_p != confirm_p:
            return False, "New passwords do not match."
        return True, ""
