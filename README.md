# Car Price Prediction

## Project Overview

This project builds a predictive model to estimate used car prices based on vehicle characteristics scraped from Auto24.ee (Estonian car marketplace).

### Key Features
- Web-scraped dataset from Auto24.ee with 15,612 car listings
- Data preprocessing and feature engineering
- Multiple model comparison (Random Forest, XGBoost, Stacking Ensembles)
- Hyperparameter optimization using GridSearchCV
- Log-transformation for handling price skewness
- Feature importance analysis and multicollinearity investigation


**Best Model Performance:**
- R² Score: 0.9436
- MAE: €2,642.59 (15.64% of median price)
- RMSE: €4,294.49 (25.41% of median price)
- Median actual price: €16,900.00

## Tools Used
- **Python 3.13+**
- **Core Libraries:**
  - pandas, numpy
  - scikit-learn
  - XGBoost
  - matplotlib, seaborn

## Project Files

- **`car_price_prediction.ipynb`** – Main notebook containing exploratory data analysis, model training, evaluation, and predictions.
- **`car_scraper.py`** – Script used to scrape used car listings and features from Auto24.ee and store them in a CSV file.
- **`auto24_cars_raw.csv`** – Raw dataset containing scraped car listings before any cleaning or preprocessing.
- **`auto24_cars_clean.csv`** – Cleaned and preprocessed dataset used for exploratory analysis and model training.
- **`prepare_data.ipynb`** – Jupyter notebook performing data cleaning, preprocessing, and feature engineering.
- **`predictions_with_urls.csv`** – File containing predicted car prices linked to their original Auto24 listing URLs.
- **`requirements.txt`** – List of Python dependencies required to run the project.
