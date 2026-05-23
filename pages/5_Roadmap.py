import streamlit as st

if "logged_in" not in st.session_state:
    st.stop()

st.title("30-Day Learning Roadmap")

if "roadmap" not in st.session_state:

    st.warning("Generate AI Analysis first from Jobs page.")

else:

    st.write(st.session_state.roadmap)