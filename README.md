# Used Car Price Predictor

An end-to-end machine learning application that estimates the resale price of a used car based on key vehicle attributes. The project covers the full pipeline from raw data to a live, containerized web application.

<p align="center">
  <img width="200" height="400" alt="ecommerce-machine-learning-use-cases" src="https://github.com/user-attachments/assets/a87ea75b-adf4-4f06-8d95-c2635dd60e2c" />
</p>
---

## Overview

Pricing a used car accurately is a non-trivial problem. The resale value depends on a combination of factors like fuel type, transmission, ownership history, mileage, and engine specifications  and the relationship between these features and price is highly non-linear. This project addresses that challenge by training a machine learning model on real-world car listing data and wrapping it in a production-ready application.

The dataset used is the **CarDekho dataset**, sourced from Kaggle, which contains listings of used cars across various makes, models, and conditions in the Indian market.

---

## How It Works

The data was first cleaned and preprocessed, missing values were handled, categorical features were encoded, and irrelevant columns were dropped. The processed data was used to train an **XGBoost Regressor**, which was chosen for its strong performance on tabular data with mixed feature types.

Once the model was trained and serialized, it was integrated into a **FastAPI** backend. The API exposes a prediction endpoint that accepts car details as input, validates the request using **Pydantic v2**, runs it through the model, and returns the predicted price. Every incoming request along with its predicted output is logged to a **SQLite** database, providing a lightweight audit trail.

The frontend is a simple **HTML/CSS/JavaScript** interface where a user can fill in the car details and get the predicted price in real time. It communicates directly with the FastAPI backend.

The entire application - backend, model, and frontend  is packaged into a **Docker** container and published to Docker Hub, making it easy to pull and run anywhere without any local setup.

---

## Model Performance

| Metric | Value |
|---|---|
| Algorithm | XGBoost Regressor |
| R2 Score | 0.941 |
| Dataset | CarDekho (Kaggle) |

---

## Project Status

The application is fully functional and containerized. Planned improvements include migrating the logging database from SQLite and deploying the container to a cloud platform for public access.

## Tech Stack

1.Data & Modelling

- Pandas, NumPy : data cleaning & preprocessing
- Scikit-learn : encoding, train-test split
- XGBoost : final regression model

2.Backend

- FastAPI : REST API framework
- Pydantic v2 : request validation
- Uvicorn : ASGI server

3.Frontend

- HTML, CSS, JavaScript

4.Storage

- SQLite : prediction logging

5.Deployment

- Docker : containerization
- Docker Hub : image registry
