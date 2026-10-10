import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"

# Load datasets
sessions = pd.read_csv(DATA_DIR / "sessions.csv")
orders = pd.read_csv(DATA_DIR / "orders.csv")
events = pd.read_csv(DATA_DIR / "events.csv")
category = pd.read_csv(DATA_DIR / "category_analysis.csv")

# Calculate overall KPIs
total_sessions = sessions["session_id"].nunique()
total_orders = orders["order_id"].nunique()
total_revenue = orders["total_amount"].sum()

conversion_rate = (
    orders["session_id"].nunique() / total_sessions * 100
    if total_sessions else 0
)

average_order_value = (
    total_revenue / total_orders
    if total_orders else 0
)

# Cart abandonment
cart_sessions = set(
    events.loc[
        events["event_type"] == "add_to_cart",
        "session_id"
    ].dropna()
)

purchase_sessions = set(orders["session_id"].dropna())

abandoned_sessions = cart_sessions - purchase_sessions

cart_abandonment_rate = (
    len(abandoned_sessions) / len(cart_sessions) * 100
    if cart_sessions else 0
)

# Create KPI summary
kpi_summary = pd.DataFrame({
    "Metric": [
        "Total Sessions",
        "Total Orders",
        "Total Revenue",
        "Conversion Rate (%)",
        "Average Order Value",
        "Cart Abandonment Rate (%)"
    ],
    "Value": [
        total_sessions,
        total_orders,
        round(total_revenue, 2),
        round(conversion_rate, 2),
        round(average_order_value, 2),
        round(cart_abandonment_rate, 2)
    ]
})

# Save dashboard data
output_file = DATA_DIR / "dashboard_kpis.csv"
kpi_summary.to_csv(output_file, index=False)

print("=" * 50)
print("SHOPMETRICS - DASHBOARD KPI SUMMARY")
print("=" * 50)
print(kpi_summary.to_string(index=False))

print("\nTOP PRODUCT CATEGORIES")
print("-" * 50)
print(
    category.sort_values(
        "total_revenue",
        ascending=False
    ).to_string(index=False)
)

print("\nDashboard data prepared successfully!")
print(f"Saved to: {output_file}")