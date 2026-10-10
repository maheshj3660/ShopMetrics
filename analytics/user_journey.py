import pandas as pd
from pathlib import Path

# Define project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"

# Load datasets
users = pd.read_csv(DATA_DIR / "users.csv")
sessions = pd.read_csv(DATA_DIR / "sessions.csv")
orders = pd.read_csv(DATA_DIR / "orders.csv")

print("=" * 45)
print("SHOPMETRICS - USER JOURNEY ANALYSIS")
print("=" * 45)

# Count sessions for each user
session_summary = sessions.groupby("user_id").agg(
    total_sessions=("session_id", "nunique"),
    first_session=("session_start", "min"),
    last_session=("session_start", "max")
).reset_index()

# Count orders and calculate spending for each user
order_summary = orders.groupby("user_id").agg(
    total_orders=("order_id", "nunique"),
    total_spent=("total_amount", "sum")
).reset_index()

# Combine information with all users
journey = users.merge(
    session_summary,
    on="user_id",
    how="left"
)

journey = journey.merge(
    order_summary,
    on="user_id",
    how="left"
)

# Replace missing activity with zero
journey["total_sessions"] = (
    journey["total_sessions"].fillna(0).astype(int)
)

journey["total_orders"] = (
    journey["total_orders"].fillna(0).astype(int)
)

journey["total_spent"] = journey["total_spent"].fillna(0)

# Save the user journey table
OUTPUT_FILE = DATA_DIR / "user_journey.csv"
journey.to_csv(OUTPUT_FILE, index=False)

# Display results
print("\nTotal users:", len(journey))
print("Users with sessions:", (journey["total_sessions"] > 0).sum())
print("Users with orders:", (journey["total_orders"] > 0).sum())
print("Total revenue: ₹", round(journey["total_spent"].sum(), 2))

print("\nUser journey table created successfully!")
print("Saved to:", OUTPUT_FILE)

print("\nSample records:")
print(journey.head())