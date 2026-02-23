from enum import IntFlag, auto

class ProductFields(IntFlag):
    NONE = 0
    ID = auto()
    NAME = auto()
    PRICE = auto()
    CATEGORY = auto()
    MANUFACTURER = auto()
    ALL = ID | NAME | PRICE | CATEGORY | MANUFACTURER


class FieldMaskBits:
    def __init__(self, mask: ProductFields):
        self.mask = mask

    @staticmethod
    def are_equal(a, b, mask):
        if mask.mask & ProductFields.ID and a.id != b.id:
            return False
        if mask.mask & ProductFields.NAME and a.name != b.name:
            return False
        if mask.mask & ProductFields.PRICE and a.price != b.price:
            return False
        if mask.mask & ProductFields.CATEGORY and a.category != b.category:
            return False
        if mask.mask & ProductFields.MANUFACTURER and a.manufacturer != b.manufacturer:
            return False
        return True

    @staticmethod
    def copy_fields(src, dst, mask):
        if mask.mask & ProductFields.NAME: dst.name = src.name
        if mask.mask & ProductFields.PRICE: dst.price = src.price
        if mask.mask & ProductFields.CATEGORY: dst.category = src.category
        if mask.mask & ProductFields.MANUFACTURER: dst.manufacturer = src.manufacturer

    @staticmethod
    def print_fields(obj, mask):
        print("----- Product Info -----")
        if mask.mask & ProductFields.ID: print("id:", obj.id)
        if mask.mask & ProductFields.NAME: print("name:", obj.name)
        if mask.mask & ProductFields.PRICE: print("price:", obj.price)
        if mask.mask & ProductFields.CATEGORY: print("category:", obj.category.value)
        if mask.mask & ProductFields.MANUFACTURER: print("manufacturer:", obj.manufacturer)
