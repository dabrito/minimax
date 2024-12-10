class Product:
    def __init__(self, id=None, name="", cost=0.0, rival_price=0.0, initial_price=0.0, min_price=0.0, max_price=0.0):
        self.id = id
        self.name = name
        self.cost = cost
        self.rival_price = rival_price
        self.initial_price = initial_price
        self.min_price = min_price
        self.max_price = max_price

    def to_dict(self):
        return {
            "name": self.name,
            "cost": self.cost,
            "rival_price": self.rival_price,
            "initial_price": self.initial_price,
            "min_price": self.min_price,
            "max_price": self.max_price,
        }

    @staticmethod
    def from_dict(data, id):
        return Product(
            id=id,
            name=data.get("name", ""),
            cost=data.get("cost", 0.0),
            rival_price=data.get("rival_price", 0.0),
            initial_price=data.get("initial_price", 0.0),
            min_price=data.get("min_price", 0.0),
            max_price=data.get("max_price", 0.0),
        )
