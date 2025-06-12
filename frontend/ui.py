import streamlit as st
import requests

API_URL = "http://localhost:8000/answer"

st.set_page_config(page_title="Deep Research", layout="centered")

st.title("🔎 Deep Research")

query = st.text_input("Ask a research question...", "")

if "steps" not in st.session_state:
    st.session_state.steps = []
if "final_answer" not in st.session_state:
    st.session_state.final_answer = ""

if st.button("Submit", type="primary", use_container_width=True) and query:
    st.session_state.steps = []
    st.session_state.final_answer = ""
    with st.spinner("Thinking..."):
        try:
            response = requests.post(API_URL, json={"text": query}, timeout=120)
            data = response.json()
            if data.get("status") == "success":
                result = data["data"]
                st.session_state.steps = result.get("steps", [])
                st.session_state.final_answer = result.get("final_answer", "")
            else:
                st.error("Backend error: " + str(data))
        except Exception as e:
            st.error(f"Error: {e}")

if st.session_state.steps:
    st.markdown("### 🧠 Thinking")
    for step in st.session_state.steps:
        st.info(f"**{step['type']}**: {step['content']}")

if st.session_state.final_answer:
    st.markdown("### ✅ Final Answer")
    st.success(st.session_state.final_answer)