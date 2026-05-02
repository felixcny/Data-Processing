import pytest
import requests

def test_api_users():
    url = "https://dummyjson.com/users"
    response = requests.get(url)
    assert response.status_code == 200
    assert "users" in response.json()

def test_api_products():
    url = "https://dummyjson.com/products"
    response = requests.get(url)
    assert response.status_code == 200
    assert "products" in response.json()

def test_api_carts():
    url = "https://dummyjson.com/carts"
    response = requests.get(url)
    assert response.status_code == 200
    assert "carts" in response.json()

