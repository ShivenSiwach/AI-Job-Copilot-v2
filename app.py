import streamlit as st
from auth import create_user, login_user

st.set_page_config(
    page_title="AI Job Copilot",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load the new light mode CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
load_css("style.css")

# Session state
for key, val in {"logged_in": False, "username": ""}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Sidebar (Clean and Light)
with st.sidebar:
    st.markdown("## 💼 AI Job Copilot")
    st.markdown("---")
    tab = st.radio("Authentication", ["Login", "Sign Up"], label_visibility="collapsed")
    st.markdown("")

    if tab == "Login":
        st.markdown("**Welcome back**")
        username = st.text_input("Username", placeholder="Enter username", key="li_user")
        password = st.text_input("Password", type="password", placeholder="Enter password", key="li_pass")
        if st.button("Login", type="primary", use_container_width=True):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username  = username
                st.success("✅ Logged in!")
                st.rerun()
            else:
                st.error("Invalid credentials.")
    else:
        st.markdown("**Create your account**")
        username = st.text_input("Username", placeholder="Choose a username", key="su_user")
        password = st.text_input("Password", type="password", placeholder="Choose a password", key="su_pass")
        if st.button("Create Account", type="primary", use_container_width=True):
            if create_user(username, password):
                st.success("Account created! Please login.")
            else:
                st.error("Username already exists.")

# Main Dashboard Layout
if not st.session_state.logged_in:
    # Top Navigation Tabs Mockup
    st.tabs(["Overview", "Features", "Pricing", "About"])
    
    #  Hero Section (Clean SaaS Style) 
    st.markdown("""
    <div class="dash-card" style="text-align: left; padding: 3rem 2rem;">
      <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">AI Job Copilot Overview</h1>
      <p style="font-size: 1.1rem; max-width: 600px;">Getting started with AI Resume Matching, Skill Gap Detection, and Career Coaching.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Split Layout (Like the image)
    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        st.markdown("""
        <div class="dash-card">
            <h4>Core Capabilities</h4>
            <br>
            <div class="list-item">
                <div><h4>📄 Resume Analysis</h4><p>AI-powered insights tailored to your career trajectory.</p></div>
            </div>
            <div class="list-item">
                <div><h4>🎯 Job Matching</h4><p>Semantic scoring to map your profile perfectly.</p></div>
            </div>
            <div class="list-item" style="border-bottom: none;">
                <div><h4>🗺️ 30-Day Roadmap</h4><p>Personalized step-by-step plans for skill gaps.</p></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with right_col:
        st.markdown("""
        <div class="dash-card">
            <h4 style="margin-bottom: 4px;">Get Started</h4>
            <p style="font-size: 12px; margin-bottom: 16px;">Create an account to access the platform.</p>
        </div>
        """, unsafe_allow_html=True)
        st.info("👈 Use the sidebar to log in or create a new account.")
else:
    st.markdown(f"<h1>Overview</h1>", unsafe_allow_html=True)
    st.markdown('<div class="dash-card">', unsafe_allow_html=True)
    st.write(f"Welcome back, **{st.session_state.username}**! Navigate using the sidebar.")
    st.markdown('</div>', unsafe_allow_html=True)
