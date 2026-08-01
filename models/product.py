"""Product model."""


class Product:
    def __init__(
        self,
        id=None,
        name=None,
        brand=None,
        category=None,
        price=0.0,
        quantity=0,
        image_path=None,
    ):
        self.id = id
        self.name = name
        self.brand = brand
        self.category = category
        self.price = float(price) if price is not None else 0.0
        self.quantity = int(quantity) if quantity is not None else 0
        self.image_path = image_path

    @property
    def total_value(self):
        return self.price * self.quantity

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "brand": self.brand,
            "category": self.category,
            "price": self.price,
            "quantity": self.quantity,
            "image_path": self.image_path,
            "total_value": self.total_value,
        }

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        if isinstance(row, dict):
            return Product(
                id=row.get("id"),
                name=row.get("name"),
                brand=row.get("brand"),
                category=row.get("category"),
                price=row.get("price"),
                quantity=row.get("quantity"),
                image_path=row.get("image_path"),
            )
        # tuple: id, name, brand, category, price, quantity, image_path
        return Product(
            id=row[0],
            name=row[1],
            brand=row[2],
            category=row[3],
            price=row[4],
            quantity=row[5],
            image_path=row[6] if len(row) > 6 else None,
        )
