import pandas as pd
import random
from datetime import datetime, timedelta

# ============================================
# SHOPMETRICS DATA GENERATOR
# ============================================

random.seed(42)

# Number of records
NUM_USERS = 5000
NUM_SESSIONS = 10000
NUM_PRODUCTS = 100

# --------------------------------------------
# 1. PRODUCTS
# --------------------------------------------

categories = [
    "Electronics",
    "Clothing",
    "Home",
    "Beauty",
    "Sports"
]

products = []

for product_id in range(1, NUM_PRODUCTS + 1):
    category = random.choice(categories)

    products.append({
        "product_id": product_id,
        "product_name": f"Product {product_id}",
        "category": category,
        "price": round(random.uniform(200, 50000), 2)
    })

products_df = pd.DataFrame(products)


# --------------------------------------------
# 2. USERS
# --------------------------------------------

start_date = datetime(2026, 1, 1)

users = []

for user_id in range(1, NUM_USERS + 1):

    signup_date = start_date + timedelta(
        days=random.randint(0, 250)
    )

    users.append({
        "user_id": user_id,
        "signup_date": signup_date.date()
    })

users_df = pd.DataFrame(users)


# --------------------------------------------
# 3. SESSIONS AND EVENTS
# --------------------------------------------

traffic_sources = [
    "Google",
    "Instagram",
    "Facebook",
    "Email",
    "Direct"
]

devices = [
    "Mobile",
    "Desktop",
    "Tablet"
]

cities = [
    "Pune",
    "Mumbai",
    "Nashik",
    "Nagpur",
    "Delhi",
    "Bangalore"
]

event_records = []
session_records = []

event_id = 1
order_id = 1
order_item_id = 1

orders = []
order_items = []

for session_number in range(1, NUM_SESSIONS + 1):

    session_id = f"S{session_number:05d}"

    user_id = random.randint(1, NUM_USERS)

    session_start = start_date + timedelta(
        days=random.randint(0, 250),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )

    session_duration = random.randint(5, 30)

    session_end = session_start + timedelta(
        minutes=session_duration
    )

    traffic_source = random.choice(traffic_sources)
    device = random.choice(devices)
    city = random.choice(cities)

    session_records.append({
        "session_id": session_id,
        "user_id": user_id,
        "session_start": session_start,
        "session_end": session_end,
        "traffic_source": traffic_source,
        "device": device,
        "city": city
    })

    # ----------------------------------------
    # PAGE VIEW
    # ----------------------------------------

    current_time = session_start + timedelta(minutes=1)

    event_records.append({
        "event_id": event_id,
        "session_id": session_id,
        "user_id": user_id,
        "event_type": "page_view",
        "product_id": None,
        "event_time": current_time
    })

    event_id += 1

    # ----------------------------------------
    # PRODUCT VIEW
    # ----------------------------------------

    product_id = random.randint(1, NUM_PRODUCTS)

    current_time += timedelta(minutes=1)

    event_records.append({
        "event_id": event_id,
        "session_id": session_id,
        "user_id": user_id,
        "event_type": "product_view",
        "product_id": product_id,
        "event_time": current_time
    })

    event_id += 1

    # ----------------------------------------
    # ADD TO CART
    # ----------------------------------------

    # Around 50% sessions add product to cart
    add_to_cart = random.random() < 0.50

    if add_to_cart:

        current_time += timedelta(minutes=1)

        event_records.append({
            "event_id": event_id,
            "session_id": session_id,
            "user_id": user_id,
            "event_type": "add_to_cart",
            "product_id": product_id,
            "event_time": current_time
        })

        event_id += 1

        # ------------------------------------
        # ORDER
        # ------------------------------------

        # Around 40% cart sessions become orders
        make_order = random.random() < 0.40

        if make_order:

            current_time += timedelta(minutes=2)

            event_records.append({
                "event_id": event_id,
                "session_id": session_id,
                "user_id": user_id,
                "event_type": "order",
                "product_id": product_id,
                "event_time": current_time
            })

            event_id += 1

            order_number = f"O{order_id:05d}"

            product_price = products_df.loc[
                products_df["product_id"] == product_id,
                "price"
            ].iloc[0]

            quantity = random.randint(1, 3)

            total_amount = round(
                product_price * quantity,
                2
            )

            orders.append({
                "order_id": order_number,
                "user_id": user_id,
                "session_id": session_id,
                "order_time": current_time,
                "total_amount": total_amount
            })

            order_items.append({
                "order_item_id": order_item_id,
                "order_id": order_number,
                "product_id": product_id,
                "quantity": quantity,
                "price": product_price
            })

            order_id += 1
            order_item_id += 1


# --------------------------------------------
# 4. CREATE DATAFRAMES
# --------------------------------------------

sessions_df = pd.DataFrame(session_records)
events_df = pd.DataFrame(event_records)
orders_df = pd.DataFrame(orders)
order_items_df = pd.DataFrame(order_items)


# --------------------------------------------
# 5. CREATE RAW DATA FOLDER
# --------------------------------------------

import os

os.makedirs("../data/raw", exist_ok=True)


# --------------------------------------------
# 6. SAVE CSV FILES
# --------------------------------------------

users_df.to_csv(
    "../data/raw/users.csv",
    index=False
)

products_df.to_csv(
    "../data/raw/products.csv",
    index=False
)

sessions_df.to_csv(
    "../data/raw/sessions.csv",
    index=False
)

events_df.to_csv(
    "../data/raw/events.csv",
    index=False
)

orders_df.to_csv(
    "../data/raw/orders.csv",
    index=False
)

order_items_df.to_csv(
    "../data/raw/order_items.csv",
    index=False
)


# --------------------------------------------
# 7. DISPLAY SUMMARY
# --------------------------------------------

print("\n====================================")
print("SHOPMETRICS DATA GENERATION COMPLETE")
print("====================================")

print(f"Users       : {len(users_df)}")
print(f"Products    : {len(products_df)}")
print(f"Sessions    : {len(sessions_df)}")
print(f"Events      : {len(events_df)}")
print(f"Orders      : {len(orders_df)}")
print(f"Order Items : {len(order_items_df)}")

print("\nCSV files created inside:")
print("../data/raw/")