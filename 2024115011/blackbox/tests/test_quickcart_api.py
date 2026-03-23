"""
QuickCart API - Black Box Testing Suite
Comprehensive automated test suite for QuickCart REST API
"""

import pytest
import requests
import json
from typing import Dict, Any, Optional

# Configuration
BASE_URL = "http://localhost:8080/api/v1"
VALID_ROLL_NUMBER = 12345
VALID_USER_ID = 1
HEADERS = {
    "X-Roll-Number": str(VALID_ROLL_NUMBER),
    "X-User-ID": str(VALID_USER_ID),
    "Content-Type": "application/json"
}
ADMIN_HEADERS = {
    "X-Roll-Number": str(VALID_ROLL_NUMBER),
    "Content-Type": "application/json"
}


class TestHeaderValidation:
    """TC-H: Test header validation"""

    def test_missing_roll_number_header(self):
        """TC-H1: Missing X-Roll-Number header should return 401"""
        headers = {"X-User-ID": str(VALID_USER_ID)}
        response = requests.get(f"{BASE_URL}/profile", headers=headers)
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"

    def test_invalid_roll_number_non_integer(self):
        """TC-H2: Invalid X-Roll-Number (non-integer) should return 400"""
        headers = {
            "X-Roll-Number": "abc",
            "X-User-ID": str(VALID_USER_ID)
        }
        response = requests.get(f"{BASE_URL}/profile", headers=headers)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    def test_invalid_roll_number_special_chars(self):
        """TC-H2b: Invalid X-Roll-Number with special chars should return 400"""
        headers = {
            "X-Roll-Number": "@#$%",
            "X-User-ID": str(VALID_USER_ID)
        }
        response = requests.get(f"{BASE_URL}/profile", headers=headers)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    def test_missing_user_id_for_user_scoped_endpoint(self):
        """TC-H3: Missing X-User-ID for user-scoped endpoint should return 400"""
        headers = {"X-Roll-Number": str(VALID_ROLL_NUMBER)}
        response = requests.get(f"{BASE_URL}/profile", headers=headers)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    def test_invalid_user_id_non_positive(self):
        """TC-H4: Invalid X-User-ID (non-positive) should return 400"""
        headers = {
            "X-Roll-Number": str(VALID_ROLL_NUMBER),
            "X-User-ID": "0"
        }
        response = requests.get(f"{BASE_URL}/profile", headers=headers)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    def test_invalid_user_id_negative(self):
        """TC-H4b: Invalid X-User-ID (negative) should return 400"""
        headers = {
            "X-Roll-Number": str(VALID_ROLL_NUMBER),
            "X-User-ID": "-5"
        }
        response = requests.get(f"{BASE_URL}/profile", headers=headers)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"


class TestProfile:
    """TC-P: Test profile endpoints"""

    def test_get_profile_valid(self):
        """TC-P1: Get profile with valid request should return 200"""
        response = requests.get(f"{BASE_URL}/profile", headers=HEADERS)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "name" in data, "Response should contain 'name'"
        assert "phone" in data, "Response should contain 'phone'"

    def test_update_profile_valid_name(self):
        """TC-P2: Update profile with valid name (2-50 chars) should succeed"""
        payload = {"name": "John Doe", "phone": "9876543210"}
        response = requests.put(f"{BASE_URL}/profile", json=payload, headers=HEADERS)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data.get("name") == "John Doe", "Name should be updated"

    def test_update_profile_name_too_short(self):
        """TC-P3: Update profile with name < 2 chars should return 400"""
        payload = {"name": "A", "phone": "9876543210"}
        response = requests.put(f"{BASE_URL}/profile", json=payload, headers=HEADERS)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    def test_update_profile_name_too_long(self):
        """TC-P4: Update profile with name > 50 chars should return 400"""
        payload = {"name": "A" * 51, "phone": "9876543210"}
        response = requests.put(f"{BASE_URL}/profile", json=payload, headers=HEADERS)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    def test_update_profile_valid_phone(self):
        """TC-P5: Update profile with valid 10-digit phone should succeed"""
        payload = {"name": "John Doe", "phone": "9876543210"}
        response = requests.put(f"{BASE_URL}/profile", json=payload, headers=HEADERS)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data.get("phone") == "9876543210", "Phone should be updated"

    def test_update_profile_phone_too_short(self):
        """TC-P6: Update profile with phone < 10 digits should return 400"""
        payload = {"name": "John Doe", "phone": "123456789"}
        response = requests.put(f"{BASE_URL}/profile", json=payload, headers=HEADERS)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    def test_update_profile_phone_too_long(self):
        """TC-P7: Update profile with phone > 10 digits should return 400"""
        payload = {"name": "John Doe", "phone": "12345678901"}
        response = requests.put(f"{BASE_URL}/profile", json=payload, headers=HEADERS)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    def test_update_profile_phone_non_numeric(self):
        """TC-P8: Update profile with non-numeric phone should return 400"""
        payload = {"name": "John Doe", "phone": "abc1234567"}
        response = requests.put(f"{BASE_URL}/profile", json=payload, headers=HEADERS)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"


class TestAddresses:
    """TC-A: Test address endpoints"""

    def test_get_addresses(self):
        """TC-A1: Get all addresses should return 200"""
        response = requests.get(f"{BASE_URL}/addresses", headers=HEADERS)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert isinstance(response.json(), list), "Response should be a list"

    def test_add_address_valid(self):
        """TC-A2: Add address with valid inputs should succeed"""
        payload = {
            "label": "HOME",
            "street": "123 Main Street",
            "city": "Mumbai",
            "pincode": "400001"
        }
        response = requests.post(f"{BASE_URL}/addresses", json=payload, headers=HEADERS)
        assert response.status_code in [200, 201], f"Expected 200/201, got {response.status_code}"
        data = response.json()
        assert "address_id" in data or "id" in data, "Response should contain address_id"
        assert data.get("label") == "HOME", "Label should match"

    def test_add_address_invalid_label(self):
        """TC-A3: Add address with invalid label should return 400"""
        payload = {
            "label": "INVALID",
            "street": "123 Main Street",
            "city": "Mumbai",
            "pincode": "400001"
        }
        response = requests.post(f"{BASE_URL}/addresses", json=payload, headers=HEADERS)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    def test_add_address_street_too_short(self):
        """TC-A4: Add address with street < 5 chars should return 400"""
        payload = {
            "label": "HOME",
            "street": "123",
            "city": "Mumbai",
            "pincode": "400001"
        }
        response = requests.post(f"{BASE_URL}/addresses", json=payload, headers=HEADERS)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    def test_add_address_street_too_long(self):
        """TC-A5: Add address with street > 100 chars should return 400"""
        payload = {
            "label": "HOME",
            "street": "A" * 101,
            "city": "Mumbai",
            "pincode": "400001"
        }
        response = requests.post(f"{BASE_URL}/addresses", json=payload, headers=HEADERS)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    def test_add_address_city_too_short(self):
        """TC-A6: Add address with city < 2 chars should return 400"""
        payload = {
            "label": "HOME",
            "street": "123 Main Street",
            "city": "M",
            "pincode": "400001"
        }
        response = requests.post(f"{BASE_URL}/addresses", json=payload, headers=HEADERS)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    def test_add_address_pincode_invalid_length(self):
        """TC-A7: Add address with pincode != 6 digits should return 400"""
        payload = {
            "label": "HOME",
            "street": "123 Main Street",
            "city": "Mumbai",
            "pincode": "40001"
        }
        response = requests.post(f"{BASE_URL}/addresses", json=payload, headers=HEADERS)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    def test_add_address_pincode_non_numeric(self):
        """TC-A8: Add address with non-numeric pincode should return 400"""
        payload = {
            "label": "HOME",
            "street": "123 Main Street",
            "city": "Mumbai",
            "pincode": "4000AB"
        }
        response = requests.post(f"{BASE_URL}/addresses", json=payload, headers=HEADERS)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    def test_delete_address_nonexistent(self):
        """TC-A13: Delete non-existent address should return 404"""
        response = requests.delete(f"{BASE_URL}/addresses/999999", headers=HEADERS)
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"


class TestProducts:
    """TC-PR: Test product endpoints"""

    def test_get_products_valid(self):
        """TC-PR1: Get all products should return 200"""
        response = requests.get(f"{BASE_URL}/products", headers=HEADERS)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert isinstance(response.json(), list), "Response should be a list"

    def test_products_only_active(self):
        """TC-PR2: Product list should only contain active products"""
        response = requests.get(f"{BASE_URL}/products", headers=HEADERS)
        products = response.json()
        for product in products:
            assert product.get("is_active", True) != False, "Inactive products should not be in list"

    def test_get_single_product_valid(self):
        """TC-PR3: Get single product by valid ID should return 200"""
        # First get a product ID from the list
        products_response = requests.get(f"{BASE_URL}/products", headers=HEADERS)
        if products_response.status_code == 200 and len(products_response.json()) > 0:
            product_id = products_response.json()[0].get("id") or products_response.json()[0].get("product_id")
            response = requests.get(f"{BASE_URL}/products/{product_id}", headers=HEADERS)
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    def test_get_single_product_invalid_id(self):
        """TC-PR4: Get product with non-existent ID should return 404"""
        response = requests.get(f"{BASE_URL}/products/999999", headers=HEADERS)
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"

    def test_filter_products_by_category(self):
        """TC-PR5: Filter products by category should work"""
        response = requests.get(f"{BASE_URL}/products?category=Electronics", headers=HEADERS)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert isinstance(response.json(), list), "Response should be a list"

    def test_search_products_by_name(self):
        """TC-PR6: Search products by name should work"""
        response = requests.get(f"{BASE_URL}/products?search=Laptop", headers=HEADERS)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert isinstance(response.json(), list), "Response should be a list"

    def test_sort_products_ascending(self):
        """TC-PR7: Sort products by price ascending should work"""
        response = requests.get(f"{BASE_URL}/products?sort=price_asc", headers=HEADERS)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        products = response.json()
        if len(products) > 1:
            prices = [p.get("price", 0) for p in products]
            assert prices == sorted(prices), "Products should be sorted ascending by price"

    def test_sort_products_descending(self):
        """TC-PR8: Sort products by price descending should work"""
        response = requests.get(f"{BASE_URL}/products?sort=price_desc", headers=HEADERS)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        products = response.json()
        if len(products) > 1:
            prices = [p.get("price", 0) for p in products]
            assert prices == sorted(prices, reverse=True), "Products should be sorted descending by price"


class TestCart:
    """TC-C: Test cart endpoints"""

    def test_get_cart_valid(self):
        """TC-C1: Get cart should return 200"""
        response = requests.get(f"{BASE_URL}/cart", headers=HEADERS)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    def test_add_item_valid_quantity(self):
        """TC-C2: Add item with valid quantity should succeed"""
        # Get a product first
        products = requests.get(f"{BASE_URL}/products", headers=HEADERS).json()
        if products:
            product_id = products[0].get("id") or products[0].get("product_id")
            payload = {"product_id": product_id, "quantity": 1}
            response = requests.post(f"{BASE_URL}/cart/add", json=payload, headers=HEADERS)
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    def test_add_item_quantity_zero(self):
        """TC-C3: Add item with quantity 0 should return 400"""
        products = requests.get(f"{BASE_URL}/products", headers=HEADERS).json()
        if products:
            product_id = products[0].get("id") or products[0].get("product_id")
            payload = {"product_id": product_id, "quantity": 0}
            response = requests.post(f"{BASE_URL}/cart/add", json=payload, headers=HEADERS)
            assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    def test_add_item_quantity_negative(self):
        """TC-C4: Add item with negative quantity should return 400"""
        products = requests.get(f"{BASE_URL}/products", headers=HEADERS).json()
        if products:
            product_id = products[0].get("id") or products[0].get("product_id")
            payload = {"product_id": product_id, "quantity": -5}
            response = requests.post(f"{BASE_URL}/cart/add", json=payload, headers=HEADERS)
            assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    def test_add_item_nonexistent_product(self):
        """TC-C5: Add non-existent product should return 404"""
        payload = {"product_id": 999999, "quantity": 1}
        response = requests.post(f"{BASE_URL}/cart/add", json=payload, headers=HEADERS)
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"

    def test_cart_subtotal_calculation(self):
        """TC-C8: Cart item subtotal should equal quantity × unit_price"""
        response = requests.get(f"{BASE_URL}/cart", headers=HEADERS)
        if response.status_code == 200:
            cart = response.json()
            for item in cart.get("items", []):
                expected_subtotal = item.get("quantity", 0) * item.get("price", 0)
                actual_subtotal = item.get("subtotal", 0)
                assert abs(actual_subtotal - expected_subtotal) < 0.01, \
                    f"Subtotal mismatch: expected {expected_subtotal}, got {actual_subtotal}"

    def test_cart_total_accuracy(self):
        """TC-C9: Cart total should be sum of all item subtotals"""
        response = requests.get(f"{BASE_URL}/cart", headers=HEADERS)
        if response.status_code == 200:
            cart = response.json()
            items = cart.get("items", [])
            expected_total = sum(item.get("subtotal", 0) for item in items)
            actual_total = cart.get("total", 0)
            assert abs(actual_total - expected_total) < 0.01, \
                f"Total mismatch: expected {expected_total}, got {actual_total}"

    def test_clear_cart(self):
        """TC-C14: Clear cart should empty it"""
        response = requests.delete(f"{BASE_URL}/cart/clear", headers=HEADERS)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        # Verify cart is empty
        cart_response = requests.get(f"{BASE_URL}/cart", headers=HEADERS)
        if cart_response.status_code == 200:
            cart = cart_response.json()
            assert len(cart.get("items", [])) == 0, "Cart should be empty"


class TestWallet:
    """TC-W: Test wallet endpoints"""

    def test_get_wallet_balance(self):
        """TC-W1: Get wallet balance should return 200"""
        response = requests.get(f"{BASE_URL}/wallet", headers=HEADERS)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "balance" in data or "amount" in data, "Response should contain balance"

    def test_add_money_zero_amount(self):
        """TC-W3: Add zero amount should return 400"""
        payload = {"amount": 0}
        response = requests.post(f"{BASE_URL}/wallet/add", json=payload, headers=HEADERS)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    def test_add_money_negative_amount(self):
        """TC-W4: Add negative amount should return 400"""
        payload = {"amount": -1000}
        response = requests.post(f"{BASE_URL}/wallet/add", json=payload, headers=HEADERS)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    def test_add_money_exceeds_maximum(self):
        """TC-W5: Add amount > 100000 should return 400"""
        payload = {"amount": 100001}
        response = requests.post(f"{BASE_URL}/wallet/add", json=payload, headers=HEADERS)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    def test_pay_from_wallet_zero_amount(self):
        """TC-W8: Pay zero amount should return 400"""
        payload = {"amount": 0}
        response = requests.post(f"{BASE_URL}/wallet/pay", json=payload, headers=HEADERS)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"


class TestLoyaltyPoints:
    """TC-LP: Test loyalty points endpoints"""

    def test_get_loyalty_points(self):
        """TC-LP1: Get loyalty points should return 200"""
        response = requests.get(f"{BASE_URL}/loyalty", headers=HEADERS)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "points" in data, "Response should contain points"

    def test_redeem_points_zero_amount(self):
        """TC-LP4: Redeem zero amount should return 400"""
        payload = {"amount": 0}
        response = requests.post(f"{BASE_URL}/loyalty/redeem", json=payload, headers=HEADERS)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"


class TestReviews:
    """TC-R: Test review endpoints"""

    def test_add_review_rating_below_minimum(self):
        """TC-R3: Add review with rating < 1 should return 400"""
        products = requests.get(f"{BASE_URL}/products", headers=HEADERS).json()
        if products:
            product_id = products[0].get("id") or products[0].get("product_id")
            payload = {"rating": 0, "comment": "Bad product"}
            response = requests.post(f"{BASE_URL}/products/{product_id}/reviews", 
                                   json=payload, headers=HEADERS)
            assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    def test_add_review_rating_above_maximum(self):
        """TC-R4: Add review with rating > 5 should return 400"""
        products = requests.get(f"{BASE_URL}/products", headers=HEADERS).json()
        if products:
            product_id = products[0].get("id") or products[0].get("product_id")
            payload = {"rating": 6, "comment": "Excellent product"}
            response = requests.post(f"{BASE_URL}/products/{product_id}/reviews", 
                                   json=payload, headers=HEADERS)
            assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    def test_add_review_comment_too_long(self):
        """TC-R6: Add review with comment > 200 chars should return 400"""
        products = requests.get(f"{BASE_URL}/products", headers=HEADERS).json()
        if products:
            product_id = products[0].get("id") or products[0].get("product_id")
            payload = {"rating": 5, "comment": "A" * 201}
            response = requests.post(f"{BASE_URL}/products/{product_id}/reviews", 
                                   json=payload, headers=HEADERS)
            assert response.status_code == 400, f"Expected 400, got {response.status_code}"


class TestSupportTickets:
    """TC-T: Test support ticket endpoints"""

    def test_create_ticket_subject_too_short(self):
        """TC-T2: Create ticket with subject < 5 chars should return 400"""
        payload = {"subject": "Help", "message": "I need assistance"}
        response = requests.post(f"{BASE_URL}/support/ticket", json=payload, headers=HEADERS)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    def test_create_ticket_subject_too_long(self):
        """TC-T3: Create ticket with subject > 100 chars should return 400"""
        payload = {"subject": "A" * 101, "message": "I need assistance"}
        response = requests.post(f"{BASE_URL}/support/ticket", json=payload, headers=HEADERS)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    def test_create_ticket_message_empty(self):
        """TC-T4: Create ticket with empty message should return 400"""
        payload = {"subject": "Help needed", "message": ""}
        response = requests.post(f"{BASE_URL}/support/ticket", json=payload, headers=HEADERS)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    def test_create_ticket_message_too_long(self):
        """TC-T5: Create ticket with message > 500 chars should return 400"""
        payload = {"subject": "Help needed", "message": "A" * 501}
        response = requests.post(f"{BASE_URL}/support/ticket", json=payload, headers=HEADERS)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    def test_get_tickets(self):
        """TC-T7: Get all tickets should return 200"""
        response = requests.get(f"{BASE_URL}/support/tickets", headers=HEADERS)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"


class TestCheckout:
    """TC-CH: Test checkout endpoint"""

    def test_checkout_empty_cart(self):
        """TC-CH6: Checkout with empty cart should return 400"""
        # Clear cart first
        requests.delete(f"{BASE_URL}/cart/clear", headers=HEADERS)
        payload = {"payment_method": "COD"}
        response = requests.post(f"{BASE_URL}/checkout", json=payload, headers=HEADERS)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    def test_checkout_invalid_payment_method(self):
        """TC-CH5: Checkout with invalid payment method should return 400"""
        payload = {"payment_method": "CRYPTO"}
        response = requests.post(f"{BASE_URL}/checkout", json=payload, headers=HEADERS)
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"


class TestAdminEndpoints:
    """TC-AD: Test admin endpoints"""

    def test_admin_get_users(self):
        """TC-AD1: Get all users (admin) should return 200"""
        response = requests.get(f"{BASE_URL}/admin/users", headers=ADMIN_HEADERS)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert isinstance(response.json(), list), "Response should be a list"

    def test_admin_get_products(self):
        """TC-AD5: Get all products (admin) should include inactive"""
        response = requests.get(f"{BASE_URL}/admin/products", headers=ADMIN_HEADERS)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert isinstance(response.json(), list), "Response should be a list"

    def test_admin_get_orders(self):
        """TC-AD4: Get all orders (admin) should return 200"""
        response = requests.get(f"{BASE_URL}/admin/orders", headers=ADMIN_HEADERS)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert isinstance(response.json(), list), "Response should be a list"

    def test_admin_get_coupons(self):
        """TC-AD6: Get all coupons (admin) should include expired"""
        response = requests.get(f"{BASE_URL}/admin/coupons", headers=ADMIN_HEADERS)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert isinstance(response.json(), list), "Response should be a list"


# Pytest fixture for test discovery
@pytest.fixture(scope="session", autouse=True)
def test_session_setup():
    """Verify API is reachable"""
    try:
        response = requests.get(f"{BASE_URL}/admin/users", headers=ADMIN_HEADERS, timeout=5)
        print(f"\n✓ API is reachable at {BASE_URL}")
        print(f"  Status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        pytest.skip("API server not running at " + BASE_URL)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
