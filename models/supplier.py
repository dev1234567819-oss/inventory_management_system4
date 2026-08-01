"""Supplier model."""


class Supplier:
    def __init__(self, id=None, name=None, contact=None, email=None, address=None):
        self.id = id
        self.name = name
        self.contact = contact
        self.email = email
        self.address = address

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "contact": self.contact,
            "email": self.email,
            "address": self.address,
        }

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        if isinstance(row, dict):
            return Supplier(
                id=row.get("id"),
                name=row.get("name"),
                contact=row.get("contact"),
                email=row.get("email"),
                address=row.get("address"),
            )
        return Supplier(
            id=row[0],
            name=row[1],
            contact=row[2],
            email=row[3],
            address=row[4],
        )
