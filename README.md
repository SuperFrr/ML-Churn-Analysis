# Churn Predictor

This project explores customer churn prediction using synthetic retail transaction data.

## Project Overview

The goal of this project is to model customer churn behavior using simulated transaction data inspired by a sports retail environment. The project includes:

- synthetic customer generation
- synthetic transaction simulation
- seasonality and playoff behavior modeling
- feature engineering using RFM-style metrics
- churn labeling using 90-day inactivity windows
- baseline logistic regression model
- exploratory data analysis in notebooks

## Current Progress

Completed:
- environment setup in VS Code
- calendar generation for 2 seasons
- customer generation
- transaction generation
- snapshot feature dataset creation
- first churn classification model
- ROC AUC evaluation
- coefficient interpretation

## Project Structure

```text
churn-predictor/
├── data/
├── notebooks/
├── src/
├── venv/