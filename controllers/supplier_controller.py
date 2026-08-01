"""Supplier controller."""

from dao.supplier_dao import SupplierDAO
from dao.purchase_dao import PurchaseDAO
from services.validation_service import ValidationService


class SupplierController:
    def __init__(self, app_controller):
        self.app = app_controller

    def get_suppliers(self, query=""):
        return SupplierDAO.get_all(query)

    def save_supplier(self, mode, name, contact, email, address, supp_id=None):
        ok, msg = ValidationService.validate_supplier(name)
        if not ok:
            return False, msg
        return SupplierDAO.save(mode, name, contact, email, address, supp_id)

    def delete_supplier(self, supp_id):
        return SupplierDAO.delete(supp_id)

    def get_purchase_history(self, supplier_name):
        return PurchaseDAO.get_by_supplier(supplier_name)
