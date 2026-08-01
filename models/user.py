"""User model."""


class User:
    def __init__(self, id=None, username=None, password=None):
        self.id = id
        self.username = username
        self.password = password

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
        }

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        if isinstance(row, dict):
            return User(
                id=row.get("id"),
                username=row.get("username"),
                password=row.get("password"),
            )
        return User(id=row[0], username=row[1], password=row[2])
