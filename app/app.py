import joblib
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- 1. GLOBAL MODEL LOADING ---
try:
    rf_model = joblib.load('fair_fare_model.pkl')
    iso_model = joblib.load('surge_detector.pkl')
    print("✅ Models loaded successfully.")
except:
    print("⚠️ Models not found. Make sure .pkl files are in the 'app' folder.")

# --- 2. THE HOMEPAGE (Fixes the 404 Error) ---
@app.route('/', methods=['GET'])
def home():
    return """
    <h1>🚖 NYC Taxi Surge System is LIVE!</h1>
    <p>The server is running correctly.</p>
    <p><b>To use the AI:</b> Send a POST request to <code style="background-color: #eee;">/predict</code></p>
    """

# --- 3. THE PREDICTION API ---
@app.route('/predict', methods=['POST'])
def predict_fare():
    try:
        data = request.get_json()
        
        # Parse Input
        features = pd.DataFrame([{
            'trip_distance': data['trip_distance'],
            'hour': data['hour'],
            'day_of_week': data['day_of_week'],
            'passenger_count': data['passenger_count']
        }])
        
        # AI Predictions
        fair_fare = rf_model.predict(features)[0]
        quoted_price = data.get('quoted_price', fair_fare)
        deviation = quoted_price - fair_fare
        
        iso_input = pd.DataFrame([{
            'deviation': deviation,
            'trip_distance': data['trip_distance']
        }])
        
        is_anomaly = iso_model.predict(iso_input)[0]
        
        return jsonify({
            'fair_fare_estimate': round(fair_fare, 2),
            'quoted_price': quoted_price,
            'is_fraudulent_surge': bool(is_anomaly == -1),
            'status': 'success'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)