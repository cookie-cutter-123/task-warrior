import requests

BASE_URL = "https://fakestoreapi.com"


def create_cart(cart_data):
    """
    Function to create a cart.
    """
    response = requests.post(f"{BASE_URL}/carts", json=cart_data)
    return response


def get_cart(cart_id):
    """
    Function to get a cart by its ID.
    """
    response = requests.get(f"{BASE_URL}/carts/{cart_id}")
    return response


def update_cart(cart_id, cart_data):
    """
    Function to update a cart by its ID.
    """
    response = requests.put(f"{BASE_URL}/carts/{cart_id}", json=cart_data)
    return response


def delete_cart(cart_id):
    """
    Function to delete a cart by its ID.
    """
    response = requests.delete(f"{BASE_URL}/carts/{cart_id}")
    return response


def list_carts():
    """
    Function to list all carts.
    """
    response = requests.get(f"{BASE_URL}/carts")
    return response
