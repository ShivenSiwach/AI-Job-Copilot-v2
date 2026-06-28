import streamlit as st
from auth import create_user, login_user

st.set_page_config(
    page_title="AI Job Copilot",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

#  Global CSS 
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background: #0f172a;
}
[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}
[data-testid="stSidebar"] .stTextInput input {
    background: #1e293b;
    border: 1px solid #334155;
    color: #f1f5f9 !important;
    border-radius: 8px;
}
[data-testid="stSidebar"] .stTextInput input:focus {
    border-color: #6366f1;
    box-shadow: 0 0 0 2px rgba(99,102,241,0.3);
}
.stButton > button {
    background: #6366f1;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1.5rem;
    font-weight: 600;
    width: 100%;
    transition: background 0.2s;
}
.stButton > button:hover {
    background: #4f46e5;
}
.hero-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 16px;
    padding: 3rem 2rem;
    text-align: center;
    color: white;
    margin-bottom: 2rem;
}
.hero-card h1 { font-size: 2.5rem; font-weight: 800; margin: 0; }
.hero-card p  { font-size: 1.1rem; opacity: 0.9; margin-top: 0.5rem; }
.feature-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-top: 1.5rem;
}
.feature-card {
    background: white;
    border-radius: 12px;
    padding: 1.25rem;
    text-align: center;
    box-shadow: 0 1px 4px rgba(0,0,0,0.07);
}
.feature-card .icon { font-size: 2rem; margin-bottom: 0.5rem; }
.feature-card h4 { font-size: 0.85rem; font-weight: 600; color: #1e293b; margin: 0; }
.feature-card p  { font-size: 0.75rem; color: #64748b; margin: 0.25rem 0 0; }
</style>
""", unsafe_allow_html=True)

#  Session state 
for key, val in {"logged_in": False, "username": ""}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Sidebar 
with st.sidebar:
    st.markdown("##  AI Job Copilot")
    st.markdown("---")
    tab = st.radio("", [" Login", " Sign Up"], label_visibility="collapsed")
    st.markdown("")

    if tab == " Login":
        st.markdown("**Welcome back**")
        username = st.text_input("Username", placeholder="Enter username", key="li_user")
        password = st.text_input("Password", type="password", placeholder="Enter password", key="li_pass")
        if st.button("Login →", use_container_width=True):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username  = username
                st.success("✅ Logged in!")
                st.rerun()
            else:
                st.error(" Invalid credentials.")

    else:
        st.markdown("**Create your account**")
        username = st.text_input("Username", placeholder="Choose a username", key="su_user")
        password = st.text_input("Password", type="password", placeholder="Choose a password", key="su_pass")
        if st.button("Create Account →", use_container_width=True):
            if create_user(username, password):
                st.success(" Account created! Please login.")
            else:
                st.error(" Username already exists.")

# Main hero 
if not st.session_state.logged_in:
    st.markdown("""
    <div class="hero-card">
      <h1> AI Job Copilot</h1>
      <p>AI Resume Matcher · Skill Gap Detector · Career Coach</p>
    </div>
    <div class="feature-grid">
      <div class="feature-card"><div class="icon"></div><h4>Resume Analysis</h4><p>AI-powered insights</p></div>
      <div class="feature-card"><div class="icon"></div><h4>Job Matching</h4><p>Semantic scoring</p></div>
      <div class="feature-card"><div class="icon"></div><h4>30-Day Roadmap</h4><p>Personalised plan</p></div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.success(f" Welcome back, **{st.session_state.username}**! Use the sidebar to navigate.")