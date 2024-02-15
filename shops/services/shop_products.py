from collections.abc import Iterable
from decimal import Decimal

from django.db import transaction

from shops.models import ShopProduct, ShopProductCategory

__all__ = ('create_shop_product', 'update_shop_product')


@transaction.atomic
def create_shop_product(
        *,
        name: str,
        price: Decimal,
        shop_group_id: int | type[int],
        category_names: Iterable[str],
) -> ShopProduct:
    category_names = set(category_names)

    product = ShopProduct.objects.create(
        name=name,
        price=price,
        shop_group_id=shop_group_id,
    )
    existing_categories = (
        ShopProductCategory.objects
        .filter(name__in=category_names)
    )
    existing_category_names = {
        category.name for category in existing_categories
    }
    new_category_names = category_names - existing_category_names

    new_categories = [
        ShopProductCategory(name=name)
        for name in new_category_names
    ]
    new_categories = ShopProductCategory.objects.bulk_create(new_categories)
    categories = list(existing_categories) + new_categories

    product.categories.add(*categories)

    return product


@transaction.atomic
def update_shop_product(
        *,
        product: ShopProduct,
        name: str,
        price: Decimal,
        category_names: Iterable[str],
        photo: str | None,
) -> ShopProduct:
    category_names = set(category_names)

    product.name = name
    product.price = price
    product.photo = photo
    product.save()

    existing_categories = list(
        ShopProductCategory.objects
        .filter(name__in=category_names)
    )
    existing_category_names = {
        category.name
        for category in existing_categories
    }
    new_category_names = category_names - existing_category_names

    new_categories = [
        ShopProductCategory(name=name)
        for name in new_category_names
    ]
    new_categories = ShopProductCategory.objects.bulk_create(new_categories)
    categories = existing_categories + new_categories

    product.categories.clear()
    product.categories.add(*categories)

    return product
