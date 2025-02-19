import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Backend API URL
API_URL = os.getenv("API_URL", "http://localhost:8000/process-voice")

# Initialize session state
if "user_text" not in st.session_state:
    st.session_state.user_text = ""

# Streamlit UI
st.set_page_config(page_title="Voice Assistant", page_icon="🎙️", layout="centered")
st.title("🗣️ AI Voice Assistant")

# User input
user_text = st.text_input("Enter your query:", value=st.session_state.user_text)

if st.button("Submit"):
    st.session_state.user_text = user_text  # Store input in session state

    with st.spinner("Processing..."):
        try:
            response = requests.post(
                API_URL,
                json={"text": user_text, "user_id": "123"},
                timeout=10
            )
            if response.status_code == 200:
                response_data = response.json()
                st.write("### 🤖 Assistant's Response:")
                st.success(response_data.get("response", "No response received."))
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
