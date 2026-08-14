from apps.catalog.models import Product


def create_product(**data):
    return Product.objects.create(**data)


def update_product(product, **data):
    for field, value in data.items():
        setattr(product, field, value)

    product.save()
    return product
