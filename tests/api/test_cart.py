import logging

from tests.api.cart_operations import (
    create_cart,
    get_cart,
    update_cart,
    delete_cart,
    list_carts
)
from tests.api.test_data import CART_DATA

# Create a logger object named after the current module
logger = logging.getLogger(__name__)


def test_create_cart():
    """
    Test creating a cart.
    """
    cart_data = CART_DATA["create"]
    response = create_cart(cart_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["userId"] == cart_data["userId"]


def test_get_cart():
    """
    Test getting a cart by its ID.
    """
    cart_id = 5

    logger.debug(f"Fetching cart ID: {cart_id}")

    response = get_cart(cart_id)
    logger.debug(f"Get cart response: {response.content}")

    assert response.status_code == 200
    response_data = response.json()
    assert response_data is not None, f"Response data is None: {response.content}"
    assert response_data["id"] == cart_id, (f"Expected cart ID {cart_id},"
                                            f"got {response_data['id']}")


def test_update_cart():
    """
    Test updating a cart by its ID.
    """
    create_data = CART_DATA["create"]
    create_response = create_cart(create_data)
    cart_id = create_response.json()["id"]

    updated_cart_data = CART_DATA["update"]
    response = update_cart(cart_id, updated_cart_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["userId"] == updated_cart_data["userId"]
    assert any(product['productId'] == 2 for product in response_data['products'])


def test_delete_cart():
    """
    Test deleting a cart by its ID.
    """
    create_data = CART_DATA["create"]
    create_response = create_cart(create_data)
    cart_id = create_response.json().get("id")
    assert cart_id is not None, "Cart ID not found in create response"

    logger.debug(f"Created cart ID: {cart_id}")

    response = delete_cart(cart_id)
    logger.debug(f"Delete cart response: {response.content}")
    assert response.status_code == 200

    get_response = get_cart(cart_id)
    logger.debug(f"Get cart after delete response: {get_response.content}")
    assert get_response.content == b'null', (f"Expected null content,"
                                             f"got {get_response.content}")


def test_list_carts():
    """
    Test listing all carts.
    """
    response = list_carts()
    assert response.status_code == 200

    response_data = response.json()
    assert isinstance(response_data, list), "Expected a list of carts"
    assert len(response_data) > 0, "Expected at least one cart in the list"

    for cart in response_data:
        assert "id" in cart, "Cart should have an 'id' field"
        assert "userId" in cart, "Cart should have a 'userId' field"
        assert "date" in cart, "Cart should have a 'date' field"
        assert "products" in cart, "Cart should have a 'products' field"
        assert isinstance(cart["products"], list), "Products should be a list"

        for product in cart["products"]:
            assert "productId" in product, ("Product should have"
                                            "a 'productId' field")
            assert "quantity" in product, ("Product should have"
                                           "a 'quantity' field")

    # Specific data checks (assuming at least one cart is always returned
    # and has valid structure)
    first_cart = response_data[0]
    assert first_cart["id"] == 1, (f"Expected cart ID to be 1,"
                                   f"got {first_cart['id']}")
    assert first_cart["userId"] == 1, (f"Expected user ID to be 1,"
                                       f"got {first_cart['userId']}")
    assert any(product["productId"] == 1 for product in first_cart["products"]), \
        "Expected at least one product with productId 1"
