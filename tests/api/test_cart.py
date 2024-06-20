from tests.api.cart_operations import (
    create_cart,
    get_cart,
    update_cart,
    delete_cart,
    list_carts
)


def test_create_cart():
    """
    Test creating a cart.
    """
    cart_data = {
        "userId": 1,
        "date": "2024-06-19",
        "products": [{"productId": 1, "quantity": 1}]
    }
    response = create_cart(cart_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["userId"] == cart_data["userId"]


def test_get_cart():
    """
    Test getting a cart by its ID.
    """
    cart_data = {
        "userId": 1,
        "date": "2024-06-19",
        "products": [{"productId": 1, "quantity": 1}]
    }
    create_response = create_cart(cart_data)
    cart_id = create_response.json()["id"]
    response = get_cart(cart_id)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["userId"] == cart_data["userId"]
    assert any(product['productId'] == 1 for product in response_data['products'])


def test_update_cart():
    """
    Test updating a cart by its ID.
    """
    cart_data = {
        "userId": 1,
        "date": "2024-06-19",
        "products": [{"productId": 1, "quantity": 1}]
    }
    create_response = create_cart(cart_data)
    cart_id = create_response.json()["id"]
    updated_cart_data = {
        "userId": 1,
        "date": "2024-06-20",
        "products": [{"productId": 2, "quantity": 2}]
    }
    response = update_cart(cart_id, updated_cart_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["userId"] == updated_cart_data["userId"]
    assert any(product['productId'] == 2 for product in response_data['products'])


def test_delete_cart():
    """
    Test deleting a cart by its ID.
    """
    cart_data = {
        "userId": 1,
        "date": "2024-06-19",
        "products": [{"productId": 1, "quantity": 1}]
    }
    create_response = create_cart(cart_data)
    cart_id = create_response.json()["id"]
    response = delete_cart(cart_id)
    assert response.status_code == 200
    get_response = get_cart(cart_id)
    assert get_response.status_code == 404


def test_list_carts():
    """
    Test listing all carts.
    """
    response = list_carts()
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
