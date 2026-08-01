"""Product controller."""

from dao.product_dao import ProductDAO
from services.validation_service import ValidationService
from utils.messagebox_util import show_error, show_info, ask_yes_no


class ProductController:
    def __init__(self, app_controller):
        self.app = app_controller

    def get_products(self, query=""):
        return ProductDAO.get_all(query)

    def get_product_names(self):
        return ProductDAO.get_product_names()

    def get_image_path(self, name):
        return ProductDAO.get_image_path(name)

    def get_low_stock(self):
        return ProductDAO.get_low_stock()

    def save_product(self, mode, name, brand, cat, price, qty, img_path, prod_id=None):
        ok, msg = ValidationService.validate_product(name, price, qty)
        if not ok:
            return False, msg
        return ProductDAO.save(mode, name, brand, cat, price, qty, img_path, prod_id)

    def delete_product(self, prod_id):
        return ProductDAO.delete(prod_id)
