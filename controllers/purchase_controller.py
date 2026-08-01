"""Purchase controller."""

from dao.purchase_dao import PurchaseDAO
from services.validation_service import ValidationService
from services.export_service import ExportService
from utils.helper import timestamp_str, open_file
from utils.messagebox_util import show_error, show_info, show_warning


class PurchaseController:
    def __init__(self, app_controller):
        self.app = app_controller

    def get_purchases(self):
        return PurchaseDAO.get_all()

    def process_purchase(
        self, item, supplier, cost_str, qty_str, export_type, file_path
    ):
        ok, msg = ValidationService.validate_purchase(
            item, supplier, cost_str, qty_str
        )
        if not ok:
            return False, msg

        cost_price = float(cost_str)
        qty = int(qty_str)
        success, result = PurchaseDAO.save(item, supplier, cost_price, qty)
        if not success:
            return False, result if isinstance(result, str) else "Failed to save purchase."

        sms_triggered = result
        ts = timestamp_str()

        if file_path:
            if export_type == "pdf":
                ExportService.export_purchase_pdf(
                    file_path, item, supplier, cost_price, qty, ts
                )
            elif export_type == "excel":
                ExportService.export_purchase_excel(
                    file_path, item, supplier, cost_price, qty, ts
                )
            open_file(file_path)

        return True, {"sms_triggered": sms_triggered, "item": item, "file_path": file_path}

    def default_invoice_name(self, item):
        return ExportService.default_invoice_name("Purchase_Invoice", item)
