# Taxi Fare Anomaly Detection System

## 1. Executive Summary
This project architects a production-grade machine learning pipeline to detect **Surge Pricing Fraud** in NYC taxi rides. It employs a dual-stage approach:
1.  **Fair Fare Engine:** A supervised **Random Forest** model that establishes a "Fair Price" benchmark based on trip physics and temporal demand ($R^2$: 0.91).
2.  **Fraud Hunter:** An unsupervised **Isolation Forest** that detects anomalies by analyzing price residuals. The system was rigorously validated using a **Synthetic "Stress Test"** protocol, achieving **95% Precision** even under simulated chaotic conditions (GPS drift/traffic variance).

---

## 2. Dataset & Engineering
The model utilizes the NYC Yellow Taxi dataset, processed through a robust data engineering pipeline.

* **Volume:** 200,000 raw trip records $\rightarrow$ **175,309 valid urban trips** after cleaning.
* **Cleaning Logic:**
    * Removed impossible outliers (Fares < $2.50 or > $500).
    * Filtered non-physical rides (0 distance, > 6 passengers).
* **Feature Engineering:**
    * **Temporal Extraction:** `Hour`, `DayOfWeek`, and `Month` to capture non-linear traffic surges.
    * **Standardization:** Applied `StandardScaler` to normalize distance and time features for model stability.

---

## 3. Methodology & Architecture

### Phase 1: Fair Price Modeling (Supervised)
* **Goal:** Predict the "Ground Truth" cost of a trip to calculate the *Residual* (Actual Price - Fair Price).
* **Algorithm:** **Random Forest Regressor** (Optimized with `max_depth=10` for low-latency inference).
* **Why Random Forest?** EDA revealed non-linear patterns (e.g., 4 AM airport spikes, 6 PM rush hour) and flat-rate rules (JFK Airport) that a Linear Regression baseline ($R^2$ 0.89) failed to capture effectively.

### Phase 2: Robust Anomaly Detection (Unsupervised)
* **Algorithm:** **Isolation Forest** trained on *Fare Residuals*.
* **Business Logic Layer:** A post-processing filter was engineered to target only **predatory overcharges** (Positive Residuals), distinguishing them from harmless undercharges or system errors.

### Phase 3: The "Stress Test" Validation
Since real-world fraud labels do not exist, I architected a **Synthetic Injection Strategy** to prove system reliability:
1.  **Fraud Injection:** Injected "Subtle Scams" (+$20 to +$80) into 5% of the test set.
2.  **Chaos Noise Injection:** Injected high-variance Gaussian noise (Scale=10) into *normal* trips to simulate extreme weather and traffic.
3.  **Dynamic Optimization:** An automated tuning loop identified the optimal decision threshold to maximize Recall while holding **Precision $\ge$ 95%**.

---

## 4. Performance Results

The models were evaluated on a strict 20% holdout set.

### Regression (Fair Pricing)
| Metric | Value | Business Context |
| :--- | :--- | :--- |
| **$R^2$ Score** | **0.91** | Explains 91% of fare variance (Beat Linear Baseline of 0.89). |
| **MAE** | **$1.58** | On average, the model predicts the fair price within $1.58. |
| **RMSE** | **$3.38** | Low variance in error, ensuring consistent user experience. |

### Anomaly Detection (Fraud)
| Metric | Value | Context |
| :--- | :--- | :--- |
| **Precision** | **95.50%** | **High Trust:** If the system flags a trip, there is a ~95% chance it is actual fraud. |
| **Recall** | **High** | Successfully caught subtle scams (+$20) even amidst simulated traffic noise. |
| **Threshold** | **~$21.50** | Optimized dynamically to filter natural outliers. |

---

## 5. Notebook Contents (`NYC_Taxi_Analysis.ipynb`)
1.  **Data Engineering:** Ingestion, Cleaning, and Temporal Feature Extraction.
2.  **Exploratory Data Analysis (EDA):**
    * *Scatter Plots:* Validated distance-price linearity and JFK flat rates.
    * *Time Series:* Validated 4 AM demand spikes.
3.  **Fair Fare Modeling:** Training Random Forest and visualizing **Feature Importance** (Distance dominance).
4.  **Robust Validation:** The "Chaos Mode" stress test code block.
5.  **Serialization:** Exporting `taxi_fraud_pipeline_v1.pkl` containing models and metadata for Docker/Flask deployment.

---

## 6. Usage Instructions

1.  **Install Dependencies:**
    ```bash
    pip install pandas numpy scikit-learn matplotlib seaborn joblib
    ```

2.  **Run the Analysis:**
    ```bash
    jupyter notebook NYC_Taxi_Analysis.ipynb
    ```

3.  **Deploy:**
    The notebook ends by generating a `pkl` file. This artifact is ready to be loaded into a microservice using:
    ```python
    import joblib
    pipeline = joblib.load('taxi_fraud_pipeline_v1.pkl')
    
    # Example Inference
    fair_price = pipeline['rf_model'].predict(new_data)
    residual = actual_price - fair_price
    is_fraud = pipeline['iso_model'].predict(residual)
    ```
