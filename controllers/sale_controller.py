"""Sale controller."""

from dao.sale_dao import SaleDAO
from services.validation_service import ValidationService
from services.export_service import ExportService
from utils.helper import timestamp_str, open_file


class SaleController:
    def __init__(self, app_controller):
        self.app = app_controller

    def get_sales(self):
        return SaleDAO.get_all()

    def process_sale(self, item, price_str, qty_str, export_type, file_path):
        ok, msg = ValidationService.validate_sale(item, price_str, qty_str)
        if not ok:
            return False, msg

        price = float(price_str)
        qty = int(qty_str)
        success, result = SaleDAO.record_sale(item, price, qty)
        if not success:
            return False, result

        total_revenue = result
        ts = timestamp_str()

        if file_path:
            if export_type == "pdf":
                ExportService.export_sale_pdf(
                    file_path, item, price, qty, total_revenue, ts
                )
            elif export_type == "excel":
                ExportService.export_sale_excel(
                    file_path, item, price, qty, total_revenue, ts
                )
            open_file(file_path)

        return True, {
            "total_revenue": total_revenue,
            "file_path": file_path,
        }

    def default_invoice_name(self, item):
        return ExportService.default_invoice_name("Invoice", item)
