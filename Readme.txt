# Analysis & Model Development

## Overview
This directory contains the Jupyter Notebook (`NYC_Taxi_Analysis.ipynb`) responsible for the exploratory data analysis (EDA), feature engineering, and model training pipeline. The primary objective was to architect a dual-model system capable of predicting fair taxi fares and isolating anomalous pricing surges indicative of fraud or system error.

## Dataset & Preprocessing
The model was trained on a dataset comprising **200,000+ trip records**.

### Data Pipeline Steps
1.  **Ingestion:** Loading historical NYC taxi trip data.
2.  **Cleaning:**
    * Removal of invalid coordinates (non-NYC lat/long).
    * Filtering of non-positive passenger counts and negative fares.
    * Handling of missing values in trip duration.
3.  **Feature Engineering:**
    * **Temporal Features:** Extracted `hour_of_day`, `day_of_week`, and `month` to capture peak traffic patterns.
    * **Geospatial Features:** Calculated Haversine distance between pickup and dropoff points.
4.  **Synthetic Anomaly Injection:** A hybrid data generation strategy was employed to create "ground truth" anomalies (simulating GPS spoofing and extreme surge pricing) to validate the unsupervised anomaly detection model.

## Methodology

### 1. Fair Fare Prediction (Regression)
* **Algorithm:** Random Forest Regressor (`sklearn.ensemble.RandomForestRegressor`).
* **Objective:** Establish a baseline "fair" price based on distance and time, independent of surge multipliers.
* **Optimization:** Hyperparameter tuning was performed on tree depth and the number of estimators to minimize overfitting.

### 2. Anomaly Detection (Classification)
* **Algorithm:** Isolation Forest (`sklearn.ensemble.IsolationForest`).
* **Objective:** Detect data points that deviate significantly from the learned distribution of standard fare-to-distance ratios.
* **Thresholding:** Calibrated contamination parameters to identify the top quantile of pricing irregularities.

## Performance Evaluation

The models were evaluated using an 80/20 train-test split.

| Model Component | Metric | Value | Description |
| :--- | :--- | :--- | :--- |
| **Regression** | **$R^2$ Score** | **0.88** | Explains 88% of the variance in fare pricing. |
| **Regression** | **MAE** | **$2.83** | Average prediction error in USD. |
| **Anomaly Detection** | **Precision** | **95%** | Success rate in identifying fraudulent/surge charges. |

## Notebook Contents
The `NYC_Taxi_Analysis.ipynb` notebook is structured as follows:
1.  **Exploratory Data Analysis (EDA):** Visualizations of pickup densities, fare distributions, and correlation matrices.
2.  **Preprocessing:** Code for cleaning and transforming raw data.
3.  **Model Training:** Implementation of Random Forest and Isolation Forest.
4.  **Evaluation:** Residual plots, feature importance charts, and metric calculations.
5.  **Serialization:** Exporting the trained models (`model.pkl`) for use in the Flask microservice.

## Usage Instructions

To replicate the analysis or retrain the models:

1.  **Install Dependencies:**
    Ensure you have the required Python libraries installed:
    ```bash
    pip install pandas numpy scikit-learn matplotlib seaborn
    ```

2.  **Launch Jupyter:**
    ```bash
    jupyter notebook NYC_Taxi_Analysis.ipynb
    ```

3.  **Execution:**
    Run all cells sequentially. The final step will save the trained model artifacts to the disk for deployment.
