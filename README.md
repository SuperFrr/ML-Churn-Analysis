# Pacers Store Customer Churn Prediction

Machine learning project that predicts whether a customer will stop purchasing from the Pacers team store within the next 90 days.

## Goal

Identify customers likely to churn and understand what behaviors drive retention.

## Dataset

Synthetic dataset simulating:

- 5,000 customers
- 2 NBA seasons
- ~43,000 transactions

Features include:
- purchase frequency
- recency
- monetary value
- discount usage
- email signup

## Model

Logistic Regression churn classifier.

Evaluation metrics:
- Precision
- Recall
- F1 Score
- ROC AUC

## Project Structure

data/
    calendar.csv
    customers.csv
    transactions.csv

src/
    calendar_generator.py
    customer_generator.py
    transaction_generator.py

notebooks/
    eda_transactions.ipynb

README.md
requirements.txt

## Future Work

- XGBoost churn model
- Feature engineering
- Customer segmentation
- Interactive churn dashboard