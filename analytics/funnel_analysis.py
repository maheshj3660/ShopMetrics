import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"

# Load event data
events = pd.read_csv(DATA_DIR / "events.csv")

# Count unique sessions at each stage
page_sessions = events.loc[
    events["event_type"] == "page_view",
    "session_id"
].nunique()

product_sessions = events.loc[
    events["event_type"] == "product_view",
    "session_id"
].nunique()

cart_sessions = events.loc[
    events["event_type"] == "add_to_cart",
    "session_id"
].nunique()

# Use actual order sessions to count purchases
orders = pd.read_csv(DATA_DIR / "orders.csv")

purchase_sessions = orders["session_id"].nunique()

# Create funnel table
funnel = pd.DataFrame({
    "Stage": [
        "Page View",
        "Product View",
        "Add to Cart",
        "Purchase"
    ],
    "Sessions": [
        page_sessions,
        product_sessions,
        cart_sessions,
        purchase_sessions
    ]
})

# Calculate conversion from the previous stage
funnel["Conversion from Previous (%)"] = (
    funnel["Sessions"] /
    funnel["Sessions"].shift(1) * 100
)

# First stage is the baseline
funnel.loc[0, "Conversion from Previous (%)"] = 100

# Calculate drop-off from the previous stage
funnel["Drop-off from Previous (%)"] = (
    100 - funnel["Conversion from Previous (%)"]
)

# Display results
print("=" * 65)
print("SHOPMETRICS - CUSTOMER FUNNEL ANALYSIS")
print("=" * 65)

print(funnel.to_string(
    index=False,
    formatters={
        "Conversion from Previous (%)": lambda x: f"{x:.2f}%",
        "Drop-off from Previous (%)": lambda x: f"{x:.2f}%"
    }
))

# Save funnel results
output_file = DATA_DIR / "funnel_analysis.csv"
funnel.to_csv(output_file, index=False)

print("\nFunnel analysis completed successfully!")
print(f"Saved to: {output_file}")