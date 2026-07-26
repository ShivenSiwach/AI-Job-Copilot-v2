import streamlit as st

st.set_page_config(page_title="30-Day Roadmap | AI Job Copilot", layout="wide")

def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass
load_css("style.css")
load_css("../style.css")

if not st.session_state.get("logged_in"):
    st.warning("Please login first."); st.stop()

st.markdown('<div class="eyebrow-label">ACTION PLAN</div>', unsafe_allow_html=True)
st.title("30-Day Learning Roadmap")

if st.session_state.get('analysis_complete'):
    st.markdown(f"""
    <div class="custom-card">
        {st.session_state['ai_roadmap']}
    </div>
    """, unsafe_allow_html=True)
else:
    st.warning("Please generate your AI Analysis first from the **Jobs** page.")
