import streamlit as st
import requests

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(page_title="Spam Detector", page_icon="✉️")

st.title("📩 Email / SMS Spam Detector")
st.write("Enter a message below and check if it's **Spam** or **Not Spam**")

# User input
user_message = st.text_area("Message", placeholder="Type your email or SMS here...")

if st.button("Predict"):
    if user_message.strip() == "":
        st.warning("⚠️ Please enter a message before predicting.")
    else:
        try:
            # Send request to FastAPI
            response = requests.post(API_URL, json={"message": user_message})
            
            if response.status_code == 200:
                result = response.json().get("prediction", "Unknown")
                
                if result == "spam":
                    st.error("🚨 This message is SPAM!")
                else:
                    st.success("✅ This message is NOT SPAM!")
            else:
                st.error(f"❌ API Error: {response.status_code}")
        except Exception as e:
            st.error(f"⚠️ Could not connect to API: {e}")
