import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv("data/processed/snapshot_churn_dataset.csv")

print("Dataset shape:", df.shape)

# -----------------------------
# Features and target
# -----------------------------
features = [
    "recency_days",
    "purchase_count",
    "total_spent",
    "avg_order_value"
]

X = df[features]
y = df["churn"]

# -----------------------------
# Train/Test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training samples:", len(X_train))
print("Test samples:", len(X_test))

# -----------------------------
# Models to compare
# -----------------------------
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(random_state=42)
}

# -----------------------------
# Train and evaluate models
# -----------------------------
for name, model in models.items():

    print("\n==============================")
    print("Model:", name)
    print("==============================")

    # Train
    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    # Evaluation
    print("\nClassification Report")
    print(classification_report(y_test, y_pred))

    roc = roc_auc_score(y_test, y_prob)
    print("ROC AUC:", roc)

    # Feature importance (tree models)
    if hasattr(model, "feature_importances_"):
        importance = pd.Series(model.feature_importances_, index=features)
        print("\nFeature Importance:")
        print(importance.sort_values(ascending=False))

    # Coefficients (logistic regression)
    if hasattr(model, "coef_"):
        importance = pd.Series(model.coef_[0], index=features)
        print("\nFeature Importance:")
        print(importance.sort_values(ascending=False))
        # Train final model (best one: Gradient Boosting)
    final_model = GradientBoostingClassifier(random_state=42)
    final_model.fit(X_train, y_train)

    joblib.dump(final_model, "models/churn_model.pkl")

    print("\nBest model saved to models/churn_model.pkl")