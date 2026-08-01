"""Dashboard controller."""

from services.report_service import ReportService


class DashboardController:
    def __init__(self, app_controller):
        self.app = app_controller

    def get_metrics(self):
        return ReportService.get_dashboard_metrics()
