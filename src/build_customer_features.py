import pandas as pd


def main():

    # Load cleaned dataset
    df = pd.read_csv("data/processed/clean_retail.csv")

    # Convert InvoiceDate to datetime
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    # Reference date for recency calculation
    reference_date = df["InvoiceDate"].max()

    # Group by CustomerID
    customer_features = df.groupby("CustomerID").agg(
        recency_days=("InvoiceDate", lambda x: (reference_date - x.max()).days),
        purchase_count=("InvoiceNo", "nunique"),
        total_spent=("total_spent", "sum")
    ).reset_index()

    # Average order value
    customer_features["avg_order_value"] = (
        customer_features["total_spent"] / customer_features["purchase_count"]
    )

    print("\nCustomer feature dataset:")
    print(customer_features.head())

    print("\nShape:", customer_features.shape)

# Save feature dataset
    output_path = "data/processed/customer_features.csv"
    customer_features.to_csv(output_path, index=False)

    print("\nCustomer features saved to:", output_path)
if __name__ == "__main__":
    main()