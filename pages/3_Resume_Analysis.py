import streamlit as st

st.set_page_config(page_title="Resume Analysis | AI Job Copilot", layout="wide")

if not st.session_state.get("logged_in"):
    st.warning(" Please login first."); st.stop()

st.title(" Resume Analysis")

# Check if the AI has run yet
if st.session_state.get('analysis_complete'):
    st.markdown(st.session_state['ai_resume'])
else:
    st.warning("Please generate your AI Analysis first from the **Jobs** page.")
