import pandas as pd


def main():
    file_path = "data/raw/OnlineRetail.xlsx"

    # Load dataset
    df = pd.read_excel(file_path)

    print("Dataset loaded.")
    print("Shape:", df.shape)

    print("\nColumns:")
    print(df.columns)

    print("\nFirst 5 rows:")
    print(df.head())

    # ----------------------------
    # Data cleaning
    # ----------------------------

    # Drop rows with missing CustomerID
    df = df.dropna(subset=["CustomerID"])

    # Remove negative or zero quantities (returns)
    df = df[df["Quantity"] > 0]

    # Remove negative prices
    df = df[df["UnitPrice"] > 0]

    print("\nCleaned shape:", df.shape)


if __name__ == "__main__":
    main()