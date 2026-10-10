import pandas as pd
from pathlib import Path

# Project folders
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# Create processed folder if it doesn't exist
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Files to clean
files = [
    "users.csv",
    "products.csv",
    "sessions.csv",
    "events.csv",
    "orders.csv",
    "order_items.csv"
]

print("SHOPMETRICS DATA CLEANING")
print("=" * 40)

for file in files:

    raw_file = RAW_DIR / file

    # Read CSV
    df = pd.read_csv(raw_file)

    print(f"\n{file}")
    print("Original rows:", len(df))

    # Remove duplicate rows
    duplicates = df.duplicated().sum()
    df = df.drop_duplicates()

    # Remove completely empty rows
    df = df.dropna(how="all")

    print("Duplicates removed:", duplicates)
    print("Final rows:", len(df))

    # Save cleaned file
    output_file = PROCESSED_DIR / file
    df.to_csv(output_file, index=False)

print("\n" + "=" * 40)
print("DATA CLEANING COMPLETE")
print("Cleaned files saved in:")
print(PROCESSED_DIR)