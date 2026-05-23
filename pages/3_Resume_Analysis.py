import streamlit as st

if "logged_in" not in st.session_state:
    st.stop()

st.title("Resume Analysis")

if "analysis" not in st.session_state:

    st.warning("Generate AI Analysis first from Jobs page.")

else:

    st.write(st.session_state.analysis)