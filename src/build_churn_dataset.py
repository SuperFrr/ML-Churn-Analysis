import pandas as pd


def main():

    # Load customer feature dataset
    df = pd.read_csv("data/processed/customer_features.csv")

    # Define churn rule
    df["churn"] = (df["recency_days"] > 90).astype(int)

    print("\nChurn dataset preview:")
    print(df.head())

    print("\nChurn distribution:")
    print(df["churn"].value_counts())

    print("\nDataset shape:", df.shape)

    # Save churn dataset
    output_path = "data/processed/churn_dataset.csv"
    df.to_csv(output_path, index=False)

    print("\nChurn dataset saved to:", output_path)


if __name__ == "__main__":
    main()