import numpy as np
import pandas as pd

def main():
    n_customers = 5000

    # --- segments (locked distribution) ---
    segments = (["dedicated"] * 1000) + (["casual"] * 2500) + (["other"] * 1500)
    rng = np.random.default_rng(42)
    rng.shuffle(segments)

    # --- signup dates: uniform across full timeline for v1 ---
    start_date = "2024-10-01"
    end_date = "2026-09-30"
    signup_dates = pd.to_datetime(
        rng.choice(pd.date_range(start_date, end_date, freq="D"), size=n_customers, replace=True)
    )

    # --- email signup probability by segment (realistic + simple) ---
    email_probs = {"dedicated": 0.75, "casual": 0.45, "other": 0.25}
    email_signup = np.array([1 if rng.random() < email_probs[s] else 0 for s in segments])

    customers_df = pd.DataFrame({
        "customer_id": np.arange(1, n_customers + 1),
        "segment": segments,
        "signup_date": signup_dates,
        "email_signup": email_signup,
    })

    customers_df.to_csv("data/customers.csv", index=False)
    print("Saved data/customers.csv")
    print(customers_df["segment"].value_counts())
    print(customers_df["email_signup"].mean())

if __name__ == "__main__":
    main()
