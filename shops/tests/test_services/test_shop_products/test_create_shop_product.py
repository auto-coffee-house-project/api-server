import pytest

from shops.services.shop_products import create_shop_product


@pytest.mark.django_db
def test_create_shop_product() -> None:
    create_shop_product()
