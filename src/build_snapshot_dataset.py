import pandas as pd
from datetime import timedelta

# -----------------------------
# Load cleaned retail dataset
# -----------------------------
df = pd.read_csv("data/processed/clean_retail.csv")

# Convert date column
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# -----------------------------
# Choose snapshot date
# -----------------------------
snapshot_date = pd.Timestamp("2011-06-01")

print("Snapshot Date:", snapshot_date)

# -----------------------------
# Split dataset
# -----------------------------
df_before = df[df["InvoiceDate"] < snapshot_date]
df_after = df[df["InvoiceDate"] >= snapshot_date]

print("Transactions before snapshot:", len(df_before))
print("Transactions after snapshot:", len(df_after))

# -----------------------------
# Build customer features
# -----------------------------
reference_date = snapshot_date

customer_features = df_before.groupby("CustomerID").agg(
    last_purchase=("InvoiceDate", "max"),
    purchase_count=("InvoiceNo", "nunique"),
    total_spent=("total_spent", "sum")
).reset_index()

# Recency
customer_features["recency_days"] = (
    reference_date - customer_features["last_purchase"]
).dt.days

# Average order value
customer_features["avg_order_value"] = (
    customer_features["total_spent"] /
    customer_features["purchase_count"]
)

# Remove temporary column
customer_features = customer_features.drop(columns=["last_purchase"])

print("Customers with features:", len(customer_features))

# -----------------------------
# Build churn labels
# -----------------------------
churn_window_end = snapshot_date + timedelta(days=90)

future_purchases = df_after[
    df_after["InvoiceDate"] <= churn_window_end
]

active_customers = future_purchases["CustomerID"].unique()

customer_features["churn"] = ~customer_features["CustomerID"].isin(active_customers)
customer_features["churn"] = customer_features["churn"].astype(int)

print("Churn distribution:")
print(customer_features["churn"].value_counts())

# -----------------------------
# Save dataset
# -----------------------------
output_path = "data/processed/snapshot_churn_dataset.csv"

customer_features.to_csv(output_path, index=False)

print("Snapshot churn dataset saved to:", output_path)

# Preview dataset
print("\nDataset preview:")
print(customer_features.head())