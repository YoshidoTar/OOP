from datetime import datetime, timedelta


class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.sold = datetime.now() - timedelta(days=100)

    def is_valid(self):
        return datetime.now() <= self.sold + timedelta(days=365)