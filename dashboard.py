import streamlit as st
import requests

# Page config
st.set_page_config(page_title="Fraud Detection", page_icon="💳")

st.title("💳 Fraud Detection UI")

# 🔹 Inputs
step = st.number_input("Step (Time)", min_value=0, value=10)

txn_type = st.selectbox("Transaction Type", [
    "PAYMENT", "TRANSFER", "CASH_OUT"
])

amount = st.number_input("Amount", min_value=0.0, value=100.0)

oldbalanceOrg = st.number_input("Old Balance (Sender)", min_value=0.0, value=1000.0)
newbalanceOrig = st.number_input("New Balance (Sender)", min_value=0.0, value=800.0)

oldbalanceDest = st.number_input("Old Balance (Receiver)", min_value=0.0, value=500.0)
newbalanceDest = st.number_input("New Balance (Receiver)", min_value=0.0, value=700.0)

# 🔹 Button
if st.button("Check Transaction"):

    # 🔥 RULE-BASED CHECK (IMPORTANT)
    sender_diff = oldbalanceOrg - newbalanceOrig
    receiver_diff = newbalanceDest - oldbalanceDest

    # Show calculation (for demo)
    st.write(f"Sender Loss: {sender_diff}")
    st.write(f"Receiver Gain: {receiver_diff}")

    # 🚨 Rule-based fraud detection
    if abs(sender_diff - receiver_diff) > 100:
        st.error("🚨 Fraud Detected (Balance mismatch rule)")
        st.warning("Reason: Sender and Receiver balance mismatch")
    else:
        # 🔹 Send to API
        data = {
            "step": step,
            "type": txn_type,
            "amount": amount,
            "oldbalanceOrg": oldbalanceOrg,
            "newbalanceOrig": newbalanceOrig,
            "oldbalanceDest": oldbalanceDest,
            "newbalanceDest": newbalanceDest
        }

        try:
            res = requests.post(
                "https://fraud-api-lrvc.onrender.com/predict",
                json=data,
                timeout=10
            )

            st.write("Status Code:", res.status_code)

            if res.status_code == 200:
                result = res.json()

                if "error" in result:
                    st.error(result["error"])
                else:
                    if result["fraud"] == 1:
                        st.error(f"🚨 Fraud! Risk Score: {result['risk_score']:.4f}")
                    else:
                        st.success(f"✅ Safe Transaction (Risk: {result['risk_score']:.4f})")

            else:
                st.error("❌ API Failed")

        except Exception as e:
            st.error(f"❌ Error: {e}")
