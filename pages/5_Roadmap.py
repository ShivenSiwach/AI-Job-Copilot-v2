import streamlit as st

st.set_page_config(page_title="30-Day Roadmap | AI Job Copilot", layout="wide")

if not st.session_state.get("logged_in"):
    st.warning(" Please login first."); st.stop()

st.title(" 30-Day Learning Roadmap")

if st.session_state.get('analysis_complete'):
    st.markdown(st.session_state['ai_roadmap'])
else:
    st.warning("Please generate your AI Analysis first from the **Jobs** page.")
