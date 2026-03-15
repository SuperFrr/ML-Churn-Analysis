import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Customer Churn Dashboard",
    page_icon="📉",
    layout="wide"
)

st.title("🧠 Customer Churn Prediction Dashboard")

# -----------------------------
# Load data
# -----------------------------
predictions = pd.read_csv("data/processed/churn_predictions.csv")
features = pd.read_csv("data/processed/snapshot_churn_dataset.csv")

df = predictions.merge(features, on="CustomerID")

# -----------------------------
# Sidebar Controls
# -----------------------------
st.sidebar.header("Dashboard Controls")

risk_filter = st.sidebar.multiselect(
    "Filter Risk Level",
    options=["LOW", "MEDIUM", "HIGH"],
    default=["LOW", "MEDIUM", "HIGH"]
)

prob_threshold = st.sidebar.slider(
    "Minimum Churn Probability",
    min_value=0.0,
    max_value=1.0,
    value=0.0,
    step=0.05
)

customer_search = st.sidebar.text_input("Search Customer ID")

# -----------------------------
# Apply Filters
# -----------------------------
filtered_df = df[df["risk_level"].isin(risk_filter)]
filtered_df = filtered_df[filtered_df["churn_probability"] >= prob_threshold]

if customer_search:
    filtered_df = filtered_df[
        filtered_df["CustomerID"].astype(str).str.contains(customer_search)
    ]

# -----------------------------
# Key Metrics
# -----------------------------
total_customers = len(filtered_df)
predicted_churn = (filtered_df["risk_level"] != "LOW").sum()
high_risk = (filtered_df["risk_level"] == "HIGH").sum()
avg_churn_prob = filtered_df["churn_probability"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", total_customers)
col2.metric("Predicted Churners", predicted_churn)
col3.metric("High Risk Customers", high_risk)
col4.metric("Avg Churn Probability", f"{avg_churn_prob:.2f}")

# -----------------------------
# Charts Section
# -----------------------------
st.subheader("Churn Probability Distribution")

col1, col2 = st.columns(2)

with col1:
    fig = px.histogram(
        filtered_df,
        x="churn_probability",
        nbins=30,
        title="Churn Probability Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    risk_counts = filtered_df["risk_level"].value_counts().reset_index()
    risk_counts.columns = ["Risk Level", "Count"]

    fig = px.bar(
        risk_counts,
        x="Risk Level",
        y="Count",
        title="Risk Level Breakdown",
        color="Risk Level"
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Top High Risk Customers
# -----------------------------
st.subheader("🔥 Top High Risk Customers")

top_risk = df.sort_values(
    "churn_probability",
    ascending=False
).head(20)

st.dataframe(
    top_risk[["CustomerID", "churn_probability", "risk_level"]],
    use_container_width=True
)

# -----------------------------
# Interactive Customer Explorer
# -----------------------------
st.subheader("🎛 Interactive Customer Explorer")

st.write("Filtered dataset")

st.dataframe(
    filtered_df[
        ["CustomerID", "churn_probability", "risk_level",
         "recency_days", "purchase_count", "total_spent", "avg_order_value"]
    ],
    use_container_width=True
)

# -----------------------------
# Revenue at Risk
# -----------------------------
st.subheader("💰 Revenue at Risk")

filtered_df["revenue_at_risk"] = (
    filtered_df["avg_order_value"] * filtered_df["churn_probability"]
)

total_revenue_risk = filtered_df["revenue_at_risk"].sum()

st.metric(
    "Estimated Revenue at Risk",
    f"${total_revenue_risk:,.2f}"
)

fig = px.histogram(
    filtered_df,
    x="revenue_at_risk",
    nbins=30,
    title="Revenue at Risk Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Feature Importance
# -----------------------------
st.subheader("📉 Feature Insights")

feature_importance = pd.DataFrame({
    "Feature": [
        "purchase_count",
        "total_spent",
        "recency_days",
        "avg_order_value"
    ],
    "Importance": [
        0.50,
        0.21,
        0.15,
        0.14
    ]
})

fig = px.bar(
    feature_importance,
    x="Feature",
    y="Importance",
    title="Feature Importance"
)

st.plotly_chart(fig, use_container_width=True)
# -----------------------------
# Customer Risk Viewer
# -----------------------------
st.subheader("🔎 Customer Risk Viewer")

customer_ids = df["CustomerID"].astype(str).unique()

selected_customer = st.selectbox(
    "Select a Customer ID",
    customer_ids
)

customer_data = df[df["CustomerID"].astype(str) == selected_customer].iloc[0]

st.write("### Customer Details")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Churn Probability",
    f"{customer_data['churn_probability']:.2f}"
)

col2.metric(
    "Risk Level",
    customer_data["risk_level"]
)

col3.metric(
    "Total Spent",
    f"${customer_data['total_spent']:.2f}"
)

# Behavior metrics
behavior_data = pd.DataFrame({
    "Metric": [
        "Recency Days",
        "Purchase Count",
        "Avg Order Value"
    ],
    "Value": [
        customer_data["recency_days"],
        customer_data["purchase_count"],
        customer_data["avg_order_value"]
    ]
})

fig = px.bar(
    behavior_data,
    x="Metric",
    y="Value",
    title="Customer Behavior Profile"
)

st.plotly_chart(fig, use_container_width=True)
# -----------------------------
# Download Customer Lists
# -----------------------------
st.subheader("⬇ Export Customer Lists")

col1, col2 = st.columns(2)

# Download filtered dataset
with col1:
    filtered_csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Filtered Customers",
        data=filtered_csv,
        file_name="filtered_customers.csv",
        mime="text/csv"
    )

# Download HIGH risk customers
with col2:
    high_risk_df = df[df["risk_level"] == "HIGH"]

    high_risk_csv = high_risk_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download High Risk Customers",
        data=high_risk_csv,
        file_name="high_risk_customers.csv",
        mime="text/csv"
    )