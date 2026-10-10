import pandas as pd
from pathlib import Path

# Define project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"

# Load datasets
events = pd.read_csv(DATA_DIR / "events.csv")
sessions = pd.read_csv(DATA_DIR / "sessions.csv")
orders = pd.read_csv(DATA_DIR / "orders.csv")

print("SHOPMETRICS - SESSION JOURNEY ANALYSIS")
print("=" * 45)

# Convert event time to datetime
events["event_time"] = pd.to_datetime(events["event_time"])

# Summarize events for each session
journey = events.groupby("session_id").agg(
    total_events=("event_id", "count"),
    product_views=("event_type", lambda x: (x == "product_view").sum()),
    cart_events=("event_type", lambda x: (x == "add_to_cart").sum()),
    checkout_events=("event_type", lambda x: (x == "checkout").sum()),
    first_event_time=("event_time", "min"),
    last_event_time=("event_time", "max")
).reset_index()

# Add session information
journey = sessions.merge(
    journey,
    on="session_id",
    how="left"
)

# Find sessions that resulted in an order
purchased_sessions = orders["session_id"].dropna().unique()

journey["purchased"] = journey["session_id"].isin(
    purchased_sessions
).map({True: "Yes", False: "No"})

# Calculate order value for each session
order_values = orders.groupby("session_id")["total_amount"].sum()

journey["order_value"] = journey["session_id"].map(order_values).fillna(0)

# Fill missing event counts with zero
count_columns = [
    "total_events",
    "product_views",
    "cart_events",
    "checkout_events"
]

journey[count_columns] = journey[count_columns].fillna(0).astype(int)

# Save session journey table
OUTPUT_FILE = DATA_DIR / "session_journey.csv"
journey.to_csv(OUTPUT_FILE, index=False)

print("Total sessions:", len(journey))
print("Sessions with purchases:", (journey["purchased"] == "Yes").sum())
print("Sessions without purchases:", (journey["purchased"] == "No").sum())

print("\nSession journey table created successfully!")
print("Saved to:", OUTPUT_FILE)

print("\nSample records:")
print(journey.head())