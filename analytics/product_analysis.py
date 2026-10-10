import pandas as pd
from pathlib import Path

# Set project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"

# Load datasets
products = pd.read_csv(DATA_DIR / "products.csv")
order_items = pd.read_csv(DATA_DIR / "order_items.csv")

# Calculate revenue for each order item
order_items["revenue"] = (
    order_items["quantity"] * order_items["price"]
)

# Merge order items with product details
product_data = order_items.merge(
    products,
    on="product_id",
    how="left"
)

# Analyse category performance
category_analysis = product_data.groupby(
    "category",
    as_index=False
).agg(
    units_sold=("quantity", "sum"),
    total_revenue=("revenue", "sum"),
    total_order_items=("order_item_id", "count")
)

# Sort categories by revenue
category_analysis = category_analysis.sort_values(
    by="total_revenue",
    ascending=False
)

# Display results
print("=" * 55)
print("SHOPMETRICS - PRODUCT CATEGORY ANALYSIS")
print("=" * 55)

print("\nCATEGORY PERFORMANCE")
print("-" * 55)

print(
    category_analysis.to_string(
        index=False,
        formatters={
            "total_revenue": lambda x: f"₹{x:,.2f}"
        }
    )
)

# Save results
OUTPUT_FILE = DATA_DIR / "category_analysis.csv"

category_analysis.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\nCategory analysis completed successfully!")
print(f"Saved to: {OUTPUT_FILE}")
# Individual Product Performance Analysis

product_analysis = product_data.groupby(
    ["product_id", "product_name", "category"],
    as_index=False
).agg(
    units_sold=("quantity", "sum"),
    total_revenue=("revenue", "sum")
)

# Sort products by revenue
product_analysis = product_analysis.sort_values(
    by="total_revenue",
    ascending=False
)

# Display top 10 products
print("\n" + "=" * 70)
print("TOP 10 PRODUCTS BY REVENUE")
print("=" * 70)

print(
    product_analysis.head(10).to_string(
        index=False,
        formatters={
            "total_revenue": lambda x: f"₹{x:,.2f}"
        }
    )
)

# Save product-level results
PRODUCT_OUTPUT = DATA_DIR / "product_performance.csv"

product_analysis.to_csv(
    PRODUCT_OUTPUT,
    index=False
)

print("\nProduct performance analysis completed successfully!")
print(f"Saved to: {PRODUCT_OUTPUT}")
# Individual Product Performance Analysis

product_analysis = product_data.groupby(
    ["product_id", "product_name", "category"],
    as_index=False
).agg(
    units_sold=("quantity", "sum"),
    total_revenue=("revenue", "sum")
)

# Sort products by revenue
product_analysis = product_analysis.sort_values(
    by="total_revenue",
    ascending=False
)

# Display top 10 products
print("\n" + "=" * 70)
print("TOP 10 PRODUCTS BY REVENUE")
print("=" * 70)

print(
    product_analysis.head(10).to_string(
        index=False,
        formatters={
            "total_revenue": lambda x: f"₹{x:,.2f}"
        }
    )
)

# Save product-level results
PRODUCT_OUTPUT = DATA_DIR / "product_performance.csv"

product_analysis.to_csv(
    PRODUCT_OUTPUT,
    index=False
)

print("\nProduct performance analysis completed successfully!")
print(f"Saved to: {PRODUCT_OUTPUT}")
# Individual Product Performance Analysis

product_analysis = product_data.groupby(
    ["product_id", "product_name", "category"],
    as_index=False
).agg(
    units_sold=("quantity", "sum"),
    total_revenue=("revenue", "sum")
)

# Sort products by revenue
product_analysis = product_analysis.sort_values(
    by="total_revenue",
    ascending=False
)

# Display top 10 products
print("\n" + "=" * 70)
print("TOP 10 PRODUCTS BY REVENUE")
print("=" * 70)

print(
    product_analysis.head(10).to_string(
        index=False,
        formatters={
            "total_revenue": lambda x: f"₹{x:,.2f}"
        }
    )
)

# Save product-level results
PRODUCT_OUTPUT = DATA_DIR / "product_performance.csv"

product_analysis.to_csv(
    PRODUCT_OUTPUT,
    index=False
)

print("\nProduct performance analysis completed successfully!")
print(f"Saved to: {PRODUCT_OUTPUT}")
# Individual Product Performance Analysis

product_analysis = product_data.groupby(
    ["product_id", "product_name", "category"],
    as_index=False
).agg(
    units_sold=("quantity", "sum"),
    total_revenue=("revenue", "sum")
)

# Sort products by revenue
product_analysis = product_analysis.sort_values(
    by="total_revenue",
    ascending=False
)

# Display top 10 products
print("\n" + "=" * 70)
print("TOP 10 PRODUCTS BY REVENUE")
print("=" * 70)

print(
    product_analysis.head(10).to_string(
        index=False,
        formatters={
            "total_revenue": lambda x: f"₹{x:,.2f}"
        }
    )
)

# Save product-level results
PRODUCT_OUTPUT = DATA_DIR / "product_performance.csv"

product_analysis.to_csv(
    PRODUCT_OUTPUT,
    index=False
)

print("\nProduct performance analysis completed successfully!")
print(f"Saved to: {PRODUCT_OUTPUT}")