import streamlit as st
import requests

st.title("💳 Fraud Detection UI")

step = st.number_input("Step", 10)
txn_type = st.selectbox("Type", ["PAYMENT", "TRANSFER", "CASH_OUT"])
amount = st.number_input("Amount", 100)

oldbalanceOrg = st.number_input("Old Balance Sender", 1000)
newbalanceOrig = st.number_input("New Balance Sender", 800)
oldbalanceDest = st.number_input("Old Balance Receiver", 500)
newbalanceDest = st.number_input("New Balance Receiver", 700)

if st.button("Check"):

    data = {
        "step": step,
        "type": txn_type,
        "amount": amount,
        "oldbalanceOrg": oldbalanceOrg,
        "newbalanceOrig": newbalanceOrig,
        "oldbalanceDest": oldbalanceDest,
        "newbalanceDest": newbalanceDest
    }

    res = requests.post("https://fraud-api-lrvc.onrender.com/predict", json=data)

    st.write("Status Code:", res.status_code)
    st.write("Response Text:", res.text)

    if res.status_code == 200:
        try:
            result = res.json()

            if "error" in result:
                st.error(result["error"])
            else:
                if result["fraud"] == 1:
                    st.error(f"🚨 Fraud! Risk: {result['risk_score']:.2f}")
                else:
                    st.success(f"✅ Safe! Risk: {result['risk_score']:.2f}")

        except:
            st.error("❌ JSON error")

    else:
        st.error("❌ API failed")
