
# App Summary

## `core`

- Shared logic, utility functions, enums, custom permissions, and abstract base models.
- Provides reusable code and components to keep the rest of the project DRY and maintainable.

## `users`

- User registration, authentication, profile management.
- Handles user addresses, roles (admin, customer), password reset, and user status.

## `products`

- Manages products, categories, brands, product images, and variants (size, color, SKU).
- Includes product reviews and ratings functionality.

## `carts`

- Handles shopping carts, cart items, and wishlists.
- Manages customer selections before checkout.

## `orders`

- Manages order creation, items within orders, order status, and shipping details.
- Handles order promotions/coupons and tracks order history.

## `payments`

- Payment processing and status tracking.
- Manages payment methods and logs payment transactions.

## `promotions`

- Manages promotional codes, discounts, and special offers.
- Handles application of coupons to orders and tracks promo code usage.

## `audit`

- Implements audit logging for key activities (create, update, delete, login, etc.).
- Enables tracking of changes and user actions for security and compliance.

***

Each app is modular and focuses on a single responsibility, making the codebase scalable, organized, and easier to maintain.
