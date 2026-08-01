"""Sale model."""


class Sale:
    def __init__(
        self,
        id=None,
        item_name=None,
        selling_price=0.0,
        quantity_sold=0,
        total_revenue=0.0,
        sale_date=None,
    ):
        self.id = id
        self.item_name = item_name
        self.selling_price = float(selling_price) if selling_price is not None else 0.0
        self.quantity_sold = int(quantity_sold) if quantity_sold is not None else 0
        self.total_revenue = (
            float(total_revenue) if total_revenue is not None else 0.0
        )
        self.sale_date = sale_date

    def to_dict(self):
        return {
            "id": self.id,
            "item_name": self.item_name,
            "selling_price": self.selling_price,
            "quantity_sold": self.quantity_sold,
            "total_revenue": self.total_revenue,
            "sale_date": self.sale_date,
        }

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        if isinstance(row, dict):
            return Sale(
                id=row.get("id"),
                item_name=row.get("item_name"),
                selling_price=row.get("selling_price"),
                quantity_sold=row.get("quantity_sold"),
                total_revenue=row.get("total_revenue"),
                sale_date=row.get("sale_date"),
            )
        return Sale(
            id=row[0],
            item_name=row[1],
            selling_price=row[2],
            quantity_sold=row[3],
            total_revenue=row[4],
            sale_date=row[5] if len(row) > 5 else None,
        )
