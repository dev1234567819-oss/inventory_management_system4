"""Dashboard metrics and profit/loss calculations."""

from dao.product_dao import ProductDAO
from dao.supplier_dao import SupplierDAO
from dao.purchase_dao import PurchaseDAO
from dao.sale_dao import SaleDAO
import config


class ReportService:
    @staticmethod
    def get_dashboard_metrics():
        """
        Returns:
            prod_count, supp_count, low_stock_items (list of (name, qty)),
            total_revenue, total_expenses
        """
        prod_count = ProductDAO.count()
        supp_count = SupplierDAO.count()
        low_stock = ProductDAO.get_low_stock(config.LOW_STOCK_THRESHOLD)
        low_stock_items = [(p.name, p.quantity) for p in low_stock]
        total_revenue = SaleDAO.get_total_revenue()
        total_expenses = PurchaseDAO.get_total_expenses()
        return prod_count, supp_count, low_stock_items, total_revenue, total_expenses

    @staticmethod
    def get_profit_loss_summary():
        total_revenue = SaleDAO.get_total_revenue()
        total_expenses = PurchaseDAO.get_total_expenses()
        net_profit = total_revenue - total_expenses
        return total_revenue, total_expenses, net_profit
