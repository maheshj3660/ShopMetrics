import pandas as pd
from pathlib import Path

# Define project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"

# Load datasets
sessions = pd.read_csv(DATA_DIR / "sessions.csv")
orders = pd.read_csv(DATA_DIR / "orders.csv")
events = pd.read_csv(DATA_DIR / "events.csv")

print("=" * 45)
print("SHOPMETRICS - BUSINESS KPI ANALYSIS")
print("=" * 45)

# 1. Conversion Rate
total_sessions = sessions["session_id"].nunique()
converted_sessions = orders["session_id"].nunique()

conversion_rate = (
    converted_sessions / total_sessions * 100
    if total_sessions > 0 else 0
)

# 2. Cart Abandonment Rate
cart_sessions = set(
    events.loc[
        events["event_type"] == "add_to_cart",
        "session_id"
    ].dropna()
)

purchase_sessions = set(
    orders["session_id"].dropna()
)

abandoned_sessions = cart_sessions - purchase_sessions

cart_session_count = len(cart_sessions)
abandoned_session_count = len(abandoned_sessions)

cart_abandonment_rate = (
    abandoned_session_count / cart_session_count * 100
    if cart_session_count > 0 else 0
)

# 3. Average Order Value (AOV)
total_orders = orders["order_id"].nunique()
total_revenue = orders["total_amount"].sum()

average_order_value = (
    total_revenue / total_orders
    if total_orders > 0 else 0
)

# Display results
print("\nKEY PERFORMANCE INDICATORS")
print("-" * 45)

print(f"Total Sessions          : {total_sessions:,}")
print(f"Converted Sessions     : {converted_sessions:,}")
print(f"Conversion Rate         : {conversion_rate:.2f}%")

print(f"\nSessions with Cart Events: {cart_session_count:,}")
print(f"Abandoned Cart Sessions  : {abandoned_session_count:,}")
print(f"Cart Abandonment Rate    : {cart_abandonment_rate:.2f}%")

print(f"\nTotal Orders             : {total_orders:,}")
print(f"Total Revenue            : ₹{total_revenue:,.2f}")
print(f"Average Order Value      : ₹{average_order_value:,.2f}")

print("\n" + "=" * 45)
print("KPI ANALYSIS COMPLETED")