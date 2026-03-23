# QuickCart API - Black Box Test Cases Design

## Overview
This document outlines comprehensive test cases for black-box testing of the QuickCart REST API. Each test case specifies input, expected output, and justification for inclusion.

---

## 1. HEADER VALIDATION TEST CASES

### TC-H1: Missing X-Roll-Number Header
- **Input**: Any endpoint without `X-Roll-Number` header
- **Expected Output**: HTTP 401
- **Justification**: API documentation mandates `X-Roll-Number` header for all requests. Missing header should be rejected.

### TC-H2: Invalid X-Roll-Number (Non-Integer)
- **Input**: `X-Roll-Number: "abc"` or `X-Roll-Number: "@#$"`
- **Expected Output**: HTTP 400
- **Justification**: Header must contain valid integer; non-integer values should return 400 error.

### TC-H3: Missing X-User-ID for User-Scoped Endpoint
- **Input**: GET `/api/v1/profile` without `X-User-ID` header
- **Expected Output**: HTTP 400
- **Justification**: User-scoped endpoints require X-User-ID; missing header should return 400.

### TC-H4: Invalid X-User-ID (Non-Positive Integer)
- **Input**: `X-User-ID: 0` or `X-User-ID: -5`
- **Expected Output**: HTTP 400
- **Justification**: X-User-ID must be positive integer; non-positive values should be rejected.

### TC-H5: Non-Existent User ID
- **Input**: `X-User-ID: 999999` (non-existent user)
- **Expected Output**: HTTP 400
- **Justification**: User-ID must match existing user in system.

---

## 2. PROFILE ENDPOINT TEST CASES

### TC-P1: Get Profile - Valid Request
- **Input**: GET `/api/v1/profile` with valid headers
- **Expected Output**: HTTP 200, User profile data (name, phone, etc.)
- **Justification**: Verify successful profile retrieval.

### TC-P2: Update Profile - Valid Name
- **Input**: PUT `/api/v1/profile` with name = "John Doe" (2-50 chars)
- **Expected Output**: HTTP 200, Updated profile data
- **Justification**: Valid name within range should be accepted.

### TC-P3: Update Profile - Name Too Short
- **Input**: PUT `/api/v1/profile` with name = "A" (1 char)
- **Expected Output**: HTTP 400
- **Justification**: Name must be 2-50 characters; shorter names should be rejected.

### TC-P4: Update Profile - Name Too Long
- **Input**: PUT `/api/v1/profile` with name = "A"*51 (51 chars)
- **Expected Output**: HTTP 400
- **Justification**: Name must be 2-50 characters; longer names should be rejected.

### TC-P5: Update Profile - Valid Phone (10 Digits)
- **Input**: PUT `/api/v1/profile` with phone = "9876543210"
- **Expected Output**: HTTP 200, Updated profile
- **Justification**: Valid 10-digit phone number should be accepted.

### TC-P6: Update Profile - Phone Too Short
- **Input**: PUT `/api/v1/profile` with phone = "123456789" (9 digits)
- **Expected Output**: HTTP 400
- **Justification**: Phone must be exactly 10 digits.

### TC-P7: Update Profile - Phone Too Long
- **Input**: PUT `/api/v1/profile` with phone = "12345678901" (11 digits)
- **Expected Output**: HTTP 400
- **Justification**: Phone must be exactly 10 digits.

### TC-P8: Update Profile - Non-Numeric Phone
- **Input**: PUT `/api/v1/profile` with phone = "abc1234567"
- **Expected Output**: HTTP 400
- **Justification**: Phone must contain only digits.

---

## 3. ADDRESSES ENDPOINT TEST CASES

### TC-A1: Get All Addresses - Valid Request
- **Input**: GET `/api/v1/addresses`
- **Expected Output**: HTTP 200, Array of user's addresses
- **Justification**: Should return all addresses for authenticated user.

### TC-A2: Add Address - Valid Inputs
- **Input**: POST `/api/v1/addresses` with label="HOME", street="123 Main Street", city="Mumbai", pincode="400001"
- **Expected Output**: HTTP 201/200, Address object with address_id
- **Justification**: Valid address should be created successfully.

### TC-A3: Add Address - Invalid Label
- **Input**: POST `/api/v1/addresses` with label="INVALID"
- **Expected Output**: HTTP 400
- **Justification**: Label must be HOME, OFFICE, or OTHER.

### TC-A4: Add Address - Street Too Short
- **Input**: POST `/api/v1/addresses` with street="123"
- **Expected Output**: HTTP 400
- **Justification**: Street must be 5-100 characters.

### TC-A5: Add Address - Street Too Long
- **Input**: POST `/api/v1/addresses` with street="A"*101
- **Expected Output**: HTTP 400
- **Justification**: Street must be 5-100 characters.

### TC-A6: Add Address - City Too Short
- **Input**: POST `/api/v1/addresses` with city="M"
- **Expected Output**: HTTP 400
- **Justification**: City must be 2-50 characters.

### TC-A7: Add Address - Pincode Invalid Length
- **Input**: POST `/api/v1/addresses` with pincode="40001" (5 digits)
- **Expected Output**: HTTP 400
- **Justification**: Pincode must be exactly 6 digits.

### TC-A8: Add Address - Pincode Non-Numeric
- **Input**: POST `/api/v1/addresses` with pincode="4000AB"
- **Expected Output**: HTTP 400
- **Justification**: Pincode must be numeric.

### TC-A9: Add Address as Default
- **Input**: POST `/api/v1/addresses` with is_default=true, when existing default exists
- **Expected Output**: HTTP 200, New address set as default, previous default updated
- **Justification**: Only one address can be default; setting new default should update existing.

### TC-A10: Update Address - Valid Street Update
- **Input**: PUT `/api/v1/addresses/{address_id}` with new street
- **Expected Output**: HTTP 200, Updated address with new street
- **Justification**: Street update should be allowed.

### TC-A11: Update Address - Cannot Change Label
- **Input**: PUT `/api/v1/addresses/{address_id}` changing label from HOME to OFFICE
- **Expected Output**: HTTP 400 or ignores change
- **Justification**: Label cannot be changed after creation.

### TC-A12: Update Address Response Shows New Data
- **Input**: PUT `/api/v1/addresses/{address_id}` with updated street
- **Expected Output**: Response must show updated data, not old data
- **Justification**: Response must reflect current state after update.

### TC-A13: Delete Address - Non-Existent ID
- **Input**: DELETE `/api/v1/addresses/999999`
- **Expected Output**: HTTP 404
- **Justification**: Deleting non-existent address should return 404.

### TC-A14: Delete Address - Valid ID
- **Input**: DELETE `/api/v1/addresses/{valid_address_id}`
- **Expected Output**: HTTP 204/200, Address removed
- **Justification**: Valid delete should succeed.

---

## 4. PRODUCTS ENDPOINT TEST CASES

### TC-PR1: Get All Products - Valid Request
- **Input**: GET `/api/v1/products`
- **Expected Output**: HTTP 200, Array of active products only
- **Justification**: Should return only active products.

### TC-PR2: Get Product - Inactive Products Not Shown
- **Input**: GET `/api/v1/products` (list view)
- **Expected Output**: No inactive products in response
- **Justification**: Inactive products must never be shown in list.

### TC-PR3: Get Single Product - Valid ID
- **Input**: GET `/api/v1/products/{valid_product_id}`
- **Expected Output**: HTTP 200, Product details
- **Justification**: Valid product lookup should succeed.

### TC-PR4: Get Single Product - Non-Existent ID
- **Input**: GET `/api/v1/products/999999`
- **Expected Output**: HTTP 404
- **Justification**: Non-existent product should return 404.

### TC-PR5: Filter Products by Category
- **Input**: GET `/api/v1/products?category=Electronics`
- **Expected Output**: HTTP 200, Products in that category only
- **Justification**: Category filtering should work correctly.

### TC-PR6: Search Products by Name
- **Input**: GET `/api/v1/products?search=Laptop`
- **Expected Output**: HTTP 200, Products matching search term
- **Justification**: Name search should return matching products.

### TC-PR7: Sort Products - Price Ascending
- **Input**: GET `/api/v1/products?sort=price_asc`
- **Expected Output**: HTTP 200, Products sorted by price ascending
- **Justification**: Ascending sort should work.

### TC-PR8: Sort Products - Price Descending
- **Input**: GET `/api/v1/products?sort=price_desc`
- **Expected Output**: HTTP 200, Products sorted by price descending
- **Justification**: Descending sort should work.

### TC-PR9: Product Price Accuracy
- **Input**: GET `/api/v1/products/{product_id}`
- **Expected Output**: Price field must match exact database price
- **Justification**: Price accuracy is critical for commerce.

---

## 5. CART ENDPOINT TEST CASES

### TC-C1: Get Empty Cart
- **Input**: GET `/api/v1/cart` for new user
- **Expected Output**: HTTP 200, Empty cart (total=0)
- **Justification**: New user should have empty cart.

### TC-C2: Add Item - Valid Quantity
- **Input**: POST `/api/v1/cart/add` with product_id, quantity=5
- **Expected Output**: HTTP 200, Item added to cart
- **Justification**: Valid item addition should succeed.

### TC-C3: Add Item - Quantity Zero
- **Input**: POST `/api/v1/cart/add` with quantity=0
- **Expected Output**: HTTP 400
- **Justification**: Quantity must be at least 1.

### TC-C4: Add Item - Negative Quantity
- **Input**: POST `/api/v1/cart/add` with quantity=-5
- **Expected Output**: HTTP 400
- **Justification**: Negative quantities should be rejected.

### TC-C5: Add Item - Non-Existent Product
- **Input**: POST `/api/v1/cart/add` with non-existent product_id
- **Expected Output**: HTTP 404
- **Justification**: Non-existent product should return 404.

### TC-C6: Add Item - Quantity Exceeds Stock
- **Input**: POST `/api/v1/cart/add` with quantity > product stock
- **Expected Output**: HTTP 400
- **Justification**: Cannot add more than available stock.

### TC-C7: Add Same Product Multiple Times - Quantities Add
- **Input**: POST `/api/v1/cart/add` with product_id=5, quantity=3; then same with quantity=2
- **Expected Output**: Cart item quantity should be 5 (3+2), not 2
- **Justification**: Quantities should accumulate, not replace.

### TC-C8: Cart Item Subtotal Accuracy
- **Input**: GET `/api/v1/cart`
- **Expected Output**: Each item subtotal = quantity × unit_price
- **Justification**: Subtotal calculation must be correct.

### TC-C9: Cart Total Accuracy
- **Input**: GET `/api/v1/cart` with multiple items
- **Expected Output**: Total = sum of all item subtotals
- **Justification**: Cart total must be accurate sum of all items.

### TC-C10: Update Item - Valid New Quantity
- **Input**: POST `/api/v1/cart/update` with quantity=10
- **Expected Output**: HTTP 200, Updated quantity
- **Justification**: Valid update should succeed.

### TC-C11: Update Item - Quantity Zero
- **Input**: POST `/api/v1/cart/update` with quantity=0
- **Expected Output**: HTTP 400
- **Justification**: Updated quantity must be at least 1.

### TC-C12: Remove Item - Valid Product in Cart
- **Input**: POST `/api/v1/cart/remove` with product_id in cart
- **Expected Output**: HTTP 200, Item removed
- **Justification**: Valid removal should succeed.

### TC-C13: Remove Item - Product Not in Cart
- **Input**: POST `/api/v1/cart/remove` with product_id not in cart
- **Expected Output**: HTTP 404
- **Justification**: Cannot remove item not in cart.

### TC-C14: Clear Cart
- **Input**: DELETE `/api/v1/cart/clear`
- **Expected Output**: HTTP 200, Cart becomes empty
- **Justification**: Clear should empty entire cart.

---

## 6. COUPON ENDPOINT TEST CASES

### TC-CP1: Apply Valid Coupon
- **Input**: POST `/api/v1/coupon/apply` with valid coupon code
- **Expected Output**: HTTP 200, Discount applied
- **Justification**: Valid coupon should be accepted.

### TC-CP2: Apply Expired Coupon
- **Input**: POST `/api/v1/coupon/apply` with expired coupon
- **Expected Output**: HTTP 400
- **Justification**: Expired coupons must be rejected.

### TC-CP3: Apply Coupon - Cart Below Minimum
- **Input**: POST `/api/v1/coupon/apply` with coupon requiring min_cart_value, cart below threshold
- **Expected Output**: HTTP 400
- **Justification**: Cart must meet minimum value requirement.

### TC-CP4: PERCENT Coupon Calculation
- **Input**: Apply PERCENT coupon with percentage=10% to cart total=1000
- **Expected Output**: Discount = 100
- **Justification**: Percentage discount calculation must be correct.

### TC-CP5: FIXED Coupon Calculation
- **Input**: Apply FIXED coupon with discount=200 to cart
- **Expected Output**: Discount = 200 (flat amount)
- **Justification**: Fixed discount must be applied exactly.

### TC-CP6: Coupon with Maximum Discount Cap
- **Input**: Apply coupon with max_discount_cap=500, calculated discount=600
- **Expected Output**: Discount capped at 500
- **Justification**: Discount must not exceed maximum cap.

### TC-CP7: Remove Coupon
- **Input**: POST `/api/v1/coupon/remove` with applied coupon
- **Expected Output**: HTTP 200, Coupon removed, discount reversed
- **Justification**: Coupon removal should work.

---

## 7. CHECKOUT ENDPOINT TEST CASES

### TC-CH1: Checkout - Valid COD
- **Input**: POST `/api/v1/checkout` with payment_method="COD", cart total ≤ 5000
- **Expected Output**: HTTP 200, Order created, payment_status="PENDING"
- **Justification**: COD valid for orders ≤ 5000.

### TC-CH2: Checkout - COD Exceeds Max
- **Input**: POST `/api/v1/checkout` with payment_method="COD", cart total > 5000
- **Expected Output**: HTTP 400
- **Justification**: COD not allowed for orders > 5000.

### TC-CH3: Checkout - Valid WALLET
- **Input**: POST `/api/v1/checkout` with payment_method="WALLET"
- **Expected Output**: HTTP 200, Order created, payment_status="PENDING"
- **Justification**: WALLET payment should work.

### TC-CH4: Checkout - Valid CARD
- **Input**: POST `/api/v1/checkout` with payment_method="CARD"
- **Expected Output**: HTTP 200, Order created, payment_status="PAID"
- **Justification**: CARD payment should be marked PAID immediately.

### TC-CH5: Checkout - Invalid Payment Method
- **Input**: POST `/api/v1/checkout` with payment_method="CRYPTO"
- **Expected Output**: HTTP 400
- **Justification**: Only COD, WALLET, CARD allowed.

### TC-CH6: Checkout - Empty Cart
- **Input**: POST `/api/v1/checkout` with empty cart
- **Expected Output**: HTTP 400
- **Justification**: Cannot checkout with empty cart.

### TC-CH7: Checkout - GST Calculation
- **Input**: POST `/api/v1/checkout` with subtotal=1000
- **Expected Output**: GST = 50 (5%), Total = 1050
- **Justification**: GST must be 5% and added once.

### TC-CH8: Checkout - No Overflow
- **Input**: POST `/api/v1/checkout` with very large cart total
- **Expected Output**: Accurate total without overflow
- **Justification**: Numerical accuracy must be maintained.

---

## 8. WALLET ENDPOINT TEST CASES

### TC-W1: Get Wallet Balance
- **Input**: GET `/api/v1/wallet`
- **Expected Output**: HTTP 200, Balance value
- **Justification**: Should return current balance.

### TC-W2: Add Money - Valid Amount
- **Input**: POST `/api/v1/wallet/add` with amount=5000
- **Expected Output**: HTTP 200, Balance increased by 5000
- **Justification**: Valid amount should be added.

### TC-W3: Add Money - Zero Amount
- **Input**: POST `/api/v1/wallet/add` with amount=0
- **Expected Output**: HTTP 400
- **Justification**: Amount must be > 0.

### TC-W4: Add Money - Negative Amount
- **Input**: POST `/api/v1/wallet/add` with amount=-1000
- **Expected Output**: HTTP 400
- **Justification**: Amount must be > 0.

### TC-W5: Add Money - Exceeds Maximum
- **Input**: POST `/api/v1/wallet/add` with amount=100001
- **Expected Output**: HTTP 400
- **Justification**: Amount must be ≤ 100000.

### TC-W6: Pay from Wallet - Valid Amount
- **Input**: POST `/api/v1/wallet/pay` with amount=1000 (sufficient balance)
- **Expected Output**: HTTP 200, Balance deducted by exact amount
- **Justification**: Exact amount should be deducted.

### TC-W7: Pay from Wallet - Insufficient Balance
- **Input**: POST `/api/v1/wallet/pay` with amount > current balance
- **Expected Output**: HTTP 400
- **Justification**: Cannot pay more than balance.

### TC-W8: Pay from Wallet - Zero Amount
- **Input**: POST `/api/v1/wallet/pay` with amount=0
- **Expected Output**: HTTP 400
- **Justification**: Amount must be > 0.

---

## 9. LOYALTY POINTS TEST CASES

### TC-LP1: Get Loyalty Points
- **Input**: GET `/api/v1/loyalty`
- **Expected Output**: HTTP 200, Current points
- **Justification**: Should return current points balance.

### TC-LP2: Redeem Points - Valid Amount
- **Input**: POST `/api/v1/loyalty/redeem` with amount=100 (sufficient points)
- **Expected Output**: HTTP 200, Points deducted
- **Justification**: Valid redemption should work.

### TC-LP3: Redeem Points - Insufficient Balance
- **Input**: POST `/api/v1/loyalty/redeem` with amount > current points
- **Expected Output**: HTTP 400
- **Justification**: Cannot redeem more than available.

### TC-LP4: Redeem Points - Zero Amount
- **Input**: POST `/api/v1/loyalty/redeem` with amount=0
- **Expected Output**: HTTP 400
- **Justification**: Amount must be at least 1.

---

## 10. ORDERS ENDPOINT TEST CASES

### TC-O1: Get All Orders
- **Input**: GET `/api/v1/orders`
- **Expected Output**: HTTP 200, Array of user's orders
- **Justification**: Should return all orders for user.

### TC-O2: Get Single Order - Valid ID
- **Input**: GET `/api/v1/orders/{valid_order_id}`
- **Expected Output**: HTTP 200, Order details
- **Justification**: Valid order lookup should work.

### TC-O3: Get Single Order - Non-Existent ID
- **Input**: GET `/api/v1/orders/999999`
- **Expected Output**: HTTP 404
- **Justification**: Non-existent order should return 404.

### TC-O4: Cancel Order - Valid Pending Order
- **Input**: POST `/api/v1/orders/{pending_order_id}/cancel`
- **Expected Output**: HTTP 200, Order cancelled
- **Justification**: Pending order should be cancellable.

### TC-O5: Cancel Order - Delivered Order
- **Input**: POST `/api/v1/orders/{delivered_order_id}/cancel`
- **Expected Output**: HTTP 400
- **Justification**: Delivered orders cannot be cancelled.

### TC-O6: Cancel Order - Non-Existent ID
- **Input**: POST `/api/v1/orders/999999/cancel`
- **Expected Output**: HTTP 404
- **Justification**: Cannot cancel non-existent order.

### TC-O7: Cancel Order - Stock Restored
- **Input**: Cancel order, then check product stock
- **Expected Output**: Stock for all items increased by order quantities
- **Justification**: Cancelled items should be returned to stock.

### TC-O8: Get Invoice - Valid Order
- **Input**: GET `/api/v1/orders/{order_id}/invoice`
- **Expected Output**: HTTP 200, Invoice with subtotal, GST, total
- **Justification**: Invoice should be generated correctly.

### TC-O9: Invoice Accuracy - Subtotal
- **Input**: GET `/api/v1/orders/{order_id}/invoice`
- **Expected Output**: Subtotal = total before GST
- **Justification**: Subtotal calculation must be correct.

### TC-O10: Invoice Accuracy - Total
- **Input**: GET `/api/v1/orders/{order_id}/invoice`
- **Expected Output**: Total must match actual order total exactly
- **Justification**: Total must be accurate.

---

## 11. REVIEWS ENDPOINT TEST CASES

### TC-R1: Get Product Reviews
- **Input**: GET `/api/v1/products/{product_id}/reviews`
- **Expected Output**: HTTP 200, Array of reviews
- **Justification**: Should return all reviews for product.

### TC-R2: Add Review - Valid Rating (1-5)
- **Input**: POST `/api/v1/products/{product_id}/reviews` with rating=4
- **Expected Output**: HTTP 200, Review created
- **Justification**: Valid rating should be accepted.

### TC-R3: Add Review - Rating Below Minimum
- **Input**: POST `/api/v1/products/{product_id}/reviews` with rating=0
- **Expected Output**: HTTP 400
- **Justification**: Rating must be 1-5.

### TC-R4: Add Review - Rating Above Maximum
- **Input**: POST `/api/v1/products/{product_id}/reviews` with rating=6
- **Expected Output**: HTTP 400
- **Justification**: Rating must be 1-5.

### TC-R5: Add Review - Valid Comment
- **Input**: POST `/api/v1/products/{product_id}/reviews` with comment (1-200 chars)
- **Expected Output**: HTTP 200, Review created
- **Justification**: Valid comment should be accepted.

### TC-R6: Add Review - Comment Too Long
- **Input**: POST `/api/v1/products/{product_id}/reviews` with comment (201 chars)
- **Expected Output**: HTTP 400
- **Justification**: Comment must be 1-200 characters.

### TC-R7: Average Rating Calculation - With Reviews
- **Input**: GET `/api/v1/products/{product_id}/reviews` (product with multiple reviews)
- **Expected Output**: Average rating = proper decimal calculation
- **Justification**: Average must be decimal, not integer.

### TC-R8: Average Rating - No Reviews
- **Input**: GET `/api/v1/products/{product_id}/reviews` (product with no reviews)
- **Expected Output**: Average rating = 0
- **Justification**: Empty review list should show 0 average.

---

## 12. SUPPORT TICKETS TEST CASES

### TC-T1: Create Ticket - Valid Input
- **Input**: POST `/api/v1/support/ticket` with subject (5-100 chars), message (1-500 chars)
- **Expected Output**: HTTP 200, Ticket created with status="OPEN"
- **Justification**: Valid ticket should be created.

### TC-T2: Create Ticket - Subject Too Short
- **Input**: POST `/api/v1/support/ticket` with subject (4 chars)
- **Expected Output**: HTTP 400
- **Justification**: Subject must be 5-100 characters.

### TC-T3: Create Ticket - Subject Too Long
- **Input**: POST `/api/v1/support/ticket` with subject (101 chars)
- **Expected Output**: HTTP 400
- **Justification**: Subject must be 5-100 characters.

### TC-T4: Create Ticket - Message Empty
- **Input**: POST `/api/v1/support/ticket` with message=""
- **Expected Output**: HTTP 400
- **Justification**: Message must be 1-500 characters.

### TC-T5: Create Ticket - Message Too Long
- **Input**: POST `/api/v1/support/ticket` with message (501 chars)
- **Expected Output**: HTTP 400
- **Justification**: Message must be 1-500 characters.

### TC-T6: Create Ticket - Message Preserved Exactly
- **Input**: POST `/api/v1/support/ticket` with special characters in message
- **Expected Output**: Message saved exactly as written
- **Justification**: Full message must be preserved.

### TC-T7: Get All Tickets
- **Input**: GET `/api/v1/support/tickets`
- **Expected Output**: HTTP 200, Array of user's tickets
- **Justification**: Should return all tickets.

### TC-T8: Update Ticket - OPEN to IN_PROGRESS
- **Input**: PUT `/api/v1/support/tickets/{ticket_id}` with status="IN_PROGRESS"
- **Expected Output**: HTTP 200, Status updated
- **Justification**: Valid status transition should work.

### TC-T9: Update Ticket - IN_PROGRESS to CLOSED
- **Input**: PUT `/api/v1/support/tickets/{ticket_id}` with status="CLOSED"
- **Expected Output**: HTTP 200, Status updated
- **Justification**: Valid status transition should work.

### TC-T10: Update Ticket - Invalid Backward Transition
- **Input**: PUT `/api/v1/support/tickets/{ticket_id}` changing CLOSED to IN_PROGRESS
- **Expected Output**: HTTP 400 or no change
- **Justification**: Status can only move forward, not backward.

### TC-T11: Update Ticket - Invalid Status
- **Input**: PUT `/api/v1/support/tickets/{ticket_id}` with status="RESOLVED"
- **Expected Output**: HTTP 400
- **Justification**: Only OPEN, IN_PROGRESS, CLOSED allowed.

---

## 13. ADMIN ENDPOINTS TEST CASES

### TC-AD1: Get All Users (Admin)
- **Input**: GET `/api/v1/admin/users` with valid X-Roll-Number
- **Expected Output**: HTTP 200, All users with wallet balances and loyalty points
- **Justification**: Admin endpoint should return full database contents.

### TC-AD2: Get Single User (Admin)
- **Input**: GET `/api/v1/admin/users/{user_id}`
- **Expected Output**: HTTP 200, Single user details
- **Justification**: Admin should be able to query any user.

### TC-AD3: Get All Carts (Admin)
- **Input**: GET `/api/v1/admin/carts`
- **Expected Output**: HTTP 200, All carts with items and totals
- **Justification**: Admin should see all carts.

### TC-AD4: Get All Orders (Admin)
- **Input**: GET `/api/v1/admin/orders`
- **Expected Output**: HTTP 200, All orders with payment and order status
- **Justification**: Admin should see all orders.

### TC-AD5: Get All Products (Admin)
- **Input**: GET `/api/v1/admin/products`
- **Expected Output**: HTTP 200, All products including inactive
- **Justification**: Admin should see all products including inactive.

### TC-AD6: Get All Coupons (Admin)
- **Input**: GET `/api/v1/admin/coupons`
- **Expected Output**: HTTP 200, All coupons including expired
- **Justification**: Admin should see all coupons including expired.

### TC-AD7: Get All Tickets (Admin)
- **Input**: GET `/api/v1/admin/tickets`
- **Expected Output**: HTTP 200, All support tickets
- **Justification**: Admin should see all tickets.

### TC-AD8: Get All Addresses (Admin)
- **Input**: GET `/api/v1/admin/addresses`
- **Expected Output**: HTTP 200, All addresses
- **Justification**: Admin should see all addresses.

---

## Test Case Summary

**Total Test Cases: 152**

| Category | Count |
|----------|-------|
| Header Validation | 5 |
| Profile | 8 |
| Addresses | 14 |
| Products | 9 |
| Cart | 14 |
| Coupons | 7 |
| Checkout | 8 |
| Wallet | 8 |
| Loyalty Points | 4 |
| Orders | 10 |
| Reviews | 8 |
| Support Tickets | 11 |
| Admin Endpoints | 8 |

---

## Test Execution Strategy

1. **Phase 1**: Header validation (TC-H1 to TC-H5)
2. **Phase 2**: Profile management (TC-P1 to TC-P8)
3. **Phase 3**: Address management (TC-A1 to TC-A14)
4. **Phase 4**: Products (TC-PR1 to TC-PR9)
5. **Phase 5**: Cart operations (TC-C1 to TC-C14)
6. **Phase 6**: Coupons (TC-CP1 to TC-CP7)
7. **Phase 7**: Checkout (TC-CH1 to TC-CH8)
8. **Phase 8**: Wallet (TC-W1 to TC-W8)
9. **Phase 9**: Loyalty Points (TC-LP1 to TC-LP4)
10. **Phase 10**: Orders (TC-O1 to TC-O10)
11. **Phase 11**: Reviews (TC-R1 to TC-R8)
12. **Phase 12**: Support Tickets (TC-T1 to TC-T11)
13. **Phase 13**: Admin endpoints (TC-AD1 to TC-AD8)

