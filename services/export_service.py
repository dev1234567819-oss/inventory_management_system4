"""Export invoices to PDF and Excel."""

import datetime
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from utils.helper import timestamp_str, safe_filename


class ExportService:
    @staticmethod
    def export_sale_pdf(file_path, item, price, qty, total, timestamp=None):
        if timestamp is None:
            timestamp = timestamp_str()
        doc = SimpleDocTemplate(
            file_path,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40,
        )
        story = []
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "TitleStyle",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=18,
            textColor=colors.HexColor("#001f3f"),
            spaceAfter=4,
        )
        sub_style = ParagraphStyle(
            "SubStyle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            textColor=colors.HexColor("#555555"),
            spaceAfter=15,
        )

        story.append(Paragraph("INVENTORY & FINANCIAL CONTROL SYSTEM", title_style))
        story.append(Paragraph("<b>Official Sales & Transaction Invoice</b>", sub_style))
        story.append(Spacer(1, 10))

        meta_data = [
            [
                Paragraph("<b>Transaction Date/Time:</b>", styles["Normal"]),
                Paragraph(timestamp, styles["Normal"]),
            ],
            [
                Paragraph("<b>Payment Status:</b>", styles["Normal"]),
                Paragraph(
                    "<font color='green'><b>PAID / COMPLETED</b></font>",
                    styles["Normal"],
                ),
            ],
        ]
        meta_table = Table(meta_data, colWidths=[150, 350])
        meta_table.setStyle(
            TableStyle(
                [
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        story.append(meta_table)
        story.append(Spacer(1, 15))

        table_data = [
            ["Item Description", "Unit Price ($)", "Quantity Sold", "Total Amount ($)"],
            [item, f"${price:.2f}", str(qty), f"${total:.2f}"],
        ]
        t = Table(table_data, colWidths=[200, 100, 90, 110])
        t.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#001f3f")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("ALIGN", (0, 0), (0, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
                ]
            )
        )
        story.append(t)
        story.append(Spacer(1, 20))

        total_data = [["Grand Total Revenue:", f"${total:.2f}"]]
        tot_table = Table(total_data, colWidths=[350, 150])
        tot_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f4f4f4")),
                    ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )
        story.append(tot_table)
        story.append(Spacer(1, 40))
        story.append(
            Paragraph(
                "<i>Thank you for your business! Inventory records have been updated automatically.</i>",
                styles["Italic"],
            )
        )
        doc.build(story)

    @staticmethod
    def export_sale_excel(file_path, item, price, qty, total, timestamp=None):
        if timestamp is None:
            timestamp = timestamp_str()
        data = {
            "Invoice Field": [
                "System Name",
                "Transaction Date & Time",
                "Item Name",
                "Unit Selling Price ($)",
                "Quantity Sold",
                "Total Revenue Generated ($)",
                "Status",
            ],
            "Details": [
                "Inventory & Financial Control System",
                timestamp,
                item,
                price,
                qty,
                total,
                "Completed & Deducted from Stock",
            ],
        }
        pd.DataFrame(data).to_excel(file_path, index=False)

    @staticmethod
    def export_purchase_pdf(file_path, item, supplier, cost_price, qty, timestamp=None):
        if timestamp is None:
            timestamp = timestamp_str()
        total_cost = float(cost_price) * int(qty)
        doc = SimpleDocTemplate(
            file_path,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40,
        )
        story = []
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "TitleStyle",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=18,
            textColor=colors.HexColor("#001f3f"),
            spaceAfter=4,
        )
        sub_style = ParagraphStyle(
            "SubStyle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            textColor=colors.HexColor("#555555"),
            spaceAfter=15,
        )

        story.append(Paragraph("INVENTORY & FINANCIAL CONTROL SYSTEM", title_style))
        story.append(
            Paragraph("<b>Official Stock Purchase & Supplier Invoice</b>", sub_style)
        )
        story.append(Spacer(1, 10))

        meta_data = [
            [
                Paragraph("<b>Supplier Name:</b>", styles["Normal"]),
                Paragraph(supplier, styles["Normal"]),
            ],
            [
                Paragraph("<b>Purchase Date/Time:</b>", styles["Normal"]),
                Paragraph(timestamp, styles["Normal"]),
            ],
            [
                Paragraph("<b>Payment Status:</b>", styles["Normal"]),
                Paragraph(
                    "<font color='green'><b>RESTOCKED / COMPLETED</b></font>",
                    styles["Normal"],
                ),
            ],
        ]
        meta_table = Table(meta_data, colWidths=[150, 350])
        meta_table.setStyle(
            TableStyle(
                [
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        story.append(meta_table)
        story.append(Spacer(1, 15))

        table_data = [
            [
                "Item Description",
                "Cost Price per Unit ($)",
                "Quantity Purchased",
                "Total Cost ($)",
            ],
            [item, f"${cost_price:.2f}", str(qty), f"${total_cost:.2f}"],
        ]
        t = Table(table_data, colWidths=[200, 110, 90, 100])
        t.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#001f3f")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("ALIGN", (0, 0), (0, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
                ]
            )
        )
        story.append(t)
        story.append(Spacer(1, 20))

        total_data = [["Total Purchase Cost:", f"${total_cost:.2f}"]]
        tot_table = Table(total_data, colWidths=[350, 150])
        tot_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f4f4f4")),
                    ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ]
            )
        )
        story.append(tot_table)
        story.append(Spacer(1, 40))
        story.append(
            Paragraph(
                "<i>Thank you! Stock catalog and expenses have been updated automatically.</i>",
                styles["Italic"],
            )
        )
        doc.build(story)

    @staticmethod
    def export_purchase_excel(
        file_path, item, supplier, cost_price, qty, timestamp=None
    ):
        if timestamp is None:
            timestamp = timestamp_str()
        total_cost = float(cost_price) * int(qty)
        data = {
            "Purchase Field": [
                "System Name",
                "Transaction Date & Time",
                "Item Name",
                "Supplier Name",
                "Cost Price per Unit ($)",
                "Quantity Purchased",
                "Total Purchase Cost ($)",
                "Status",
            ],
            "Details": [
                "Inventory & Financial Control System",
                timestamp,
                item,
                supplier,
                float(cost_price),
                int(qty),
                total_cost,
                "Completed & Added to Stock",
            ],
        }
        pd.DataFrame(data).to_excel(file_path, index=False)

    @staticmethod
    def default_invoice_name(prefix, item):
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{safe_filename(item)}_{ts}"
