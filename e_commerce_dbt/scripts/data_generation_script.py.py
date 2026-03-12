from faker import Faker
import pandas as pd
import random

fake = Faker()

# -----------------------------
# CONFIG
# -----------------------------

NUM_USERS = 1000
NUM_PRODUCTS = 200
NUM_ORDERS = 5000
NUM_ORDER_ITEMS = 12000

countries = ["USA", "UK", "Canada", "Germany", "India", "France"]
categories = ["Electronics", "Clothing", "Home", "Books", "Sports", "Beauty"]

# -----------------------------
# USERS
# -----------------------------

users = []

for user_id in range(1, NUM_USERS + 1):
    users.append({
        "user_id": user_id,
        "full_name": fake.name(),
        "email": fake.email(),
        "country": random.choice(countries),
        "signup_date": fake.date_between(start_date="-2y", end_date="today")
    })

users_df = pd.DataFrame(users)
users_df.to_csv("users.csv", index=False)

print("users.csv created")

# -----------------------------
# PRODUCTS
# -----------------------------

products = []

for product_id in range(1, NUM_PRODUCTS + 1):
    products.append({
        "product_id": product_id,
        "product_name": fake.word().capitalize() + " Product",
        "category": random.choice(categories),
        "price": round(random.uniform(10, 500), 2)
    })

products_df = pd.DataFrame(products)
products_df.to_csv("products.csv", index=False)

print("products.csv created")

# -----------------------------
# ORDERS
# -----------------------------

orders = []

for order_id in range(1, NUM_ORDERS + 1):
    orders.append({
        "order_id": order_id,
        "user_id": random.randint(1, NUM_USERS),
        "order_date": fake.date_between(start_date="-1y", end_date="today"),
        "status": random.choice(["completed", "pending", "shipped"])
    })

orders_df = pd.DataFrame(orders)
orders_df.to_csv("orders.csv", index=False)

print("orders.csv created")

# -----------------------------
# ORDER ITEMS
# -----------------------------

order_items = []

for item_id in range(1, NUM_ORDER_ITEMS + 1):

    product_id = random.randint(1, NUM_PRODUCTS)
    quantity = random.randint(1, 5)

    price = round(random.uniform(10, 500), 2)

    order_items.append({
        "order_item_id": item_id,
        "order_id": random.randint(1, NUM_ORDERS),
        "product_id": product_id,
        "quantity": quantity,
        "unit_price": price
    })

order_items_df = pd.DataFrame(order_items)
order_items_df.to_csv("order_items.csv", index=False)

print("order_items.csv created")

print("All CSV files generated successfully!")