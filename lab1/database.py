from field_mask import FieldMaskBits, ProductFields

class ProductRepository:
    def __init__(self):
        self._data = []

    def add(self, product):
        self._data.append(product)

    def get_all(self):
        return self._data

    def find_by_name(self, name: str):
        return [p for p in self._data if p.name.lower() == name.lower()]

    def merge_by_mask(self, mask: FieldMaskBits):
        merged = []
        for product in self._data:
            if any(FieldMaskBits.are_equal(product, m, mask) for m in merged):
                continue
            merged.append(product)
        self._data = merged

    def copy_data(self, source, equal_mask: FieldMaskBits, copy_mask: FieldMaskBits):
        for p in self._data:
            if FieldMaskBits.are_equal(p, source, equal_mask):
                FieldMaskBits.copy_fields(source, p, copy_mask)
