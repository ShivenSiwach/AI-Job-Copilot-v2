import streamlit as st

if "logged_in" not in st.session_state:
    st.stop()

st.title("Resume Analysis")

if st.session_state.get('analysis_complete'):
    # The data exists, render the UI!
    st.write(st.session_state['resume_data'])
else:
    st.warning("Generate AI Analysis first from Jobs page.")
