from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load model
model = joblib.load("fraud_model.pkl")

@app.route("/")
def home():
    return "API Running"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)
        print("DATA RECEIVED:", data)

        # 🔥 TYPE ENCODING (SAFE)
        mapping = {"PAYMENT": 0,"TRANSFER": 1,"CASH_OUT": 2}
        txn_type = mapping.get(data.get("type"), 0)
        # 🔥 SAFE NUMERIC CONVERSION
        step = int(float(data.get("step", 0)))
        amount = float(data.get("amount", 0))

        oldOrg = float(data.get("oldbalanceOrg", 0))
        newOrig = float(data.get("newbalanceOrig", 0))

        oldDest = float(data.get("oldbalanceDest", 0))
        newDest = float(data.get("newbalanceDest", 0))

        # 🔥 FEATURE ENGINEERING
        hour = step % 24
        is_night = 1 if hour < 6 else 0

        balance_diff_orig = oldOrg - newOrig
        balance_diff_dest = newDest - oldDest

        error_balance_orig = amount - balance_diff_orig
        error_balance_dest = amount - balance_diff_dest

        is_zero_balance = 1 if oldOrg == 0 else 0
        amount_ratio = amount / (oldOrg + 1)

        # 🔥 FINAL FEATURES (IMPORTANT ORDER)
        features = np.array([[
            step,
            txn_type,
            amount,
            oldOrg,
            newOrig,
            oldDest,
            newDest,
            hour,
            is_night,
            balance_diff_orig,
            balance_diff_dest,
            error_balance_orig,
            error_balance_dest,
            is_zero_balance,
            amount_ratio
        ]], dtype=float)

        print("FEATURES:", features)

        # 🔥 MODEL PREDICTION
        prediction = model.predict(features)[0]
        prob = model.predict_proba(features)[0][1]

        return jsonify({
            "fraud": int(prediction),
            "risk_score": float(prob)
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 200  # always return JSON

if __name__ == "__main__":
    app.run(debug=True)