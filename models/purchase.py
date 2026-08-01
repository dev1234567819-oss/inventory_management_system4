"""Purchase model."""


class Purchase:
    def __init__(
        self,
        id=None,
        item_name=None,
        supplier_name=None,
        cost_price=0.0,
        quantity=0,
        purchase_date=None,
    ):
        self.id = id
        self.item_name = item_name
        self.supplier_name = supplier_name
        self.cost_price = float(cost_price) if cost_price is not None else 0.0
        self.quantity = int(quantity) if quantity is not None else 0
        self.purchase_date = purchase_date

    @property
    def total_cost(self):
        return self.cost_price * self.quantity

    def to_dict(self):
        return {
            "id": self.id,
            "item_name": self.item_name,
            "supplier_name": self.supplier_name,
            "cost_price": self.cost_price,
            "quantity": self.quantity,
            "purchase_date": self.purchase_date,
            "total_cost": self.total_cost,
        }

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        if isinstance(row, dict):
            return Purchase(
                id=row.get("id"),
                item_name=row.get("item_name"),
                supplier_name=row.get("supplier_name"),
                cost_price=row.get("cost_price"),
                quantity=row.get("quantity"),
                purchase_date=row.get("purchase_date"),
            )
        return Purchase(
            id=row[0],
            item_name=row[1],
            supplier_name=row[2],
            cost_price=row[3],
            quantity=row[4],
            purchase_date=row[5] if len(row) > 5 else None,
        )
