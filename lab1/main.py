from models import Product, ProductCategory
from database import ProductRepository
from field_mask import FieldMaskBits, ProductFields

def main():
    repo = ProductRepository()

    repo.add(Product(1, "Laptop", 1500.0, ProductCategory.ELECTRONICS, "Dell"))
    repo.add(Product(2, "Laptop", 1200.0, ProductCategory.ELECTRONICS, "HP"))
    repo.add(Product(3, "Bread", 2.5, ProductCategory.FOOD, "Local"))

    print("FindByName('Laptop'):")
    laptops = repo.find_by_name("Laptop")
    for p in laptops:
        FieldMaskBits.print_fields(p, FieldMaskBits(ProductFields.ALL))

    print("\nMerge by mask (Name + Category):")
    mask_merge = FieldMaskBits(ProductFields.NAME | ProductFields.CATEGORY)
    repo.merge_by_mask(mask_merge)

    print("\nAfter merge:")
    for p in repo.get_all():
        FieldMaskBits.print_fields(p, FieldMaskBits(ProductFields.ALL))

    print("\nCopy data (price) from new Laptop to existing ones:")
    source = Product(0, "Laptop", 999.99, ProductCategory.ELECTRONICS, "Acer")
    repo.copy_data(source,
                   equal_mask=FieldMaskBits(ProductFields.NAME | ProductFields.CATEGORY),
                   copy_mask=FieldMaskBits(ProductFields.PRICE))

    for p in repo.get_all():
        FieldMaskBits.print_fields(p, FieldMaskBits(ProductFields.ALL))


if __name__ == "__main__":
    main()
