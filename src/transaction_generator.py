import pandas as pd
import numpy as np


def main():

    # -----------------------------
    # Load data
    # -----------------------------
    calendar_df = pd.read_csv("data/calendar.csv", parse_dates=["date"])
    customers_df = pd.read_csv("data/customers.csv", parse_dates=["signup_date"])

    rng = np.random.default_rng(42)

    transactions = []
    transaction_id = 1

    # -----------------------------
    # Base in-season daily purchase rates
    # -----------------------------
    base_rates = {
        "dedicated": 0.05,
        "casual": 0.02,
        "other": 0.01
    }

    # Discount probabilities by segment
    discount_probs = {
        "dedicated": 0.20,
        "casual": 0.40,
        "other": 0.65
    }

    # -----------------------------
    # Loop through customers
    # -----------------------------
    for _, customer in customers_df.iterrows():

        segment = customer["segment"]
        signup_date = customer["signup_date"]
        email_signup = customer["email_signup"]

        for _, day in calendar_df.iterrows():

            current_date = day["date"]

            # Skip days before signup
            if current_date < signup_date:
                continue

            # Start with base rate
            purchase_prob = base_rates[segment]

            # -----------------------------
            # Offseason adjustment (70% drop)
            # -----------------------------
            if day["season_phase"] == "offseason":
                purchase_prob *= 0.3

            # -----------------------------
            # Playoff multiplier
            # -----------------------------
            if day["season_phase"] == "playoff":
                if segment == "dedicated":
                    purchase_prob *= 1.5
                elif segment == "casual":
                    purchase_prob *= 2.0
                else:
                    purchase_prob *= 2.5

            # -----------------------------
            # Season 2 performance boost
            # -----------------------------
            if day["is_season2"]:
                if segment == "dedicated":
                    purchase_prob *= 1.1
                elif segment == "casual":
                    purchase_prob *= 1.2
                else:
                    purchase_prob *= 1.25

            # -----------------------------
            # Email structural boost
            # -----------------------------
            if email_signup == 1:
                purchase_prob *= 1.05

            # -----------------------------
            # Simulate purchase
            # -----------------------------
            if rng.random() < purchase_prob:

                # Generate subtotal by segment
                if segment == "dedicated":
                    subtotal = rng.normal(120, 40)
                elif segment == "casual":
                    subtotal = rng.normal(75, 30)
                else:
                    subtotal = rng.normal(50, 25)

                # Prevent negative or unrealistic values
                subtotal = max(10, subtotal)

                # Discount logic
                discount_used = 1 if rng.random() < discount_probs[segment] else 0

                if discount_used:
                    discount_percent = rng.uniform(0.10, 0.40)
                    discount_amount = subtotal * discount_percent
                else:
                    discount_percent = 0
                    discount_amount = 0

                total_spent = subtotal - discount_amount

                transactions.append({
                    "transaction_id": transaction_id,
                    "customer_id": customer["customer_id"],
                    "purchase_date": current_date,
                    "subtotal": round(subtotal, 2),
                    "discount_used": discount_used,
                    "discount_percent": round(discount_percent, 2),
                    "total_spent": round(total_spent, 2)
                })

                transaction_id += 1

    transactions_df = pd.DataFrame(transactions)

    transactions_df.to_csv("data/transactions.csv", index=False)

    print("Transactions generated.")
    print("Total transactions:", len(transactions_df))
    print("Unique purchasing customers:", transactions_df["customer_id"].nunique())
    print("\nPurchase distribution per customer:")
    print(transactions_df.groupby("customer_id").size().describe())

    print("\nMonetary summary:")
    print(transactions_df[["subtotal", "total_spent"]].describe())

    print("\nDiscount usage rate:")
    print(transactions_df["discount_used"].mean())


if __name__ == "__main__":
    main()
