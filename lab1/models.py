from enum import Enum

class ProductCategory(Enum):
    FOOD = "Food"
    ELECTRONICS = "Electronics"
    CLOTHING = "Clothing"
    FURNITURE = "Furniture"


class Product:
    def __init__(self, id_: int, name: str, price: float, category: ProductCategory, manufacturer: str):
        self.id = id_
        self.name = name
        self.price = price
        self.category = category
        self.manufacturer = manufacturer

    def __repr__(self):
        return f"Product(id={self.id}, name={self.name}, price={self.price}, category={self.category.value}, manufacturer={self.manufacturer})"
