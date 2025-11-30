import requests
import json

# The URL of your local API
# Note: Ensure your Flask app is running in a separate terminal before running this!
url = 'http://127.0.0.1:5000/predict'

# ---------------------------------------------------------
# TEST CASE 1: NORMAL TRIP (Fair Price)
# ---------------------------------------------------------
# Scenario: A standard 2-mile trip at 10 AM on a Tuesday.
# Expected: "is_fraudulent_surge": false
normal_payload = {
    "trip_distance": 2.0,
    "hour": 10,
    "day_of_week": 1,        # Tuesday
    "passenger_count": 1,
    "quoted_price": 8.0      # Reasonable price ($2.50 base + 2 miles * $2.50)
}

# ---------------------------------------------------------
# TEST CASE 2: FRAUD TRIP (The "CV Claim")
# ---------------------------------------------------------
# Scenario: The same 2-mile trip, but the app quotes $50.00.
# Expected: "is_fraudulent_surge": true
fraud_payload = {
    "trip_distance": 2.0,
    "hour": 10,
    "day_of_week": 1,
    "passenger_count": 1,
    "quoted_price": 50.0     # MASSIVE SURGE (Anomaly)
}

def send_request(tag, data):
    print(f"\n🚀 Sending {tag} Request...")
    try:
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS!")
            print(f"   - Fair Fare Estimate: ${result['fair_fare_estimate']}")
            print(f"   - User Quoted Price:  ${result['quoted_price']}")
            print(f"   - FRAUD DETECTED?:    {result['is_fraudulent_surge']}")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Is the Flask server running? (Run 'python app.py' first)")

if __name__ == "__main__":
    send_request("NORMAL", normal_payload)
    send_request("FRAUD", fraud_payload)