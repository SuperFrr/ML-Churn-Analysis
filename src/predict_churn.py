import pandas as pd
import joblib

# -----------------------------
# Load trained model
# -----------------------------
model = joblib.load("models/churn_model.pkl")

print("Model loaded.")

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv("data/processed/snapshot_churn_dataset.csv")

# Features used by model
features = [
    "recency_days",
    "purchase_count",
    "total_spent",
    "avg_order_value"
]

X = df[features]

# -----------------------------
# Generate predictions
# -----------------------------
df["churn_probability"] = model.predict_proba(X)[:, 1]

# -----------------------------
# Assign risk levels
# -----------------------------
def risk_level(prob):

    if prob >= 0.75:
        return "HIGH"
    elif prob >= 0.40:
        return "MEDIUM"
    else:
        return "LOW"

df["risk_level"] = df["churn_probability"].apply(risk_level)

# -----------------------------
# Output predictions
# -----------------------------
output = df[[
    "CustomerID",
    "churn_probability",
    "risk_level"
]]

# Save predictions
output_path = "data/processed/churn_predictions.csv"

output.to_csv(output_path, index=False)

print("\nPredictions saved to:", output_path)

# Preview
print("\nPrediction preview:")
print(output.head())