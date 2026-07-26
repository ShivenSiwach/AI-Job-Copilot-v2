import streamlit as st
from auth import create_user, login_user

st.set_page_config(
    page_title="AI Job Copilot",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- FRAME.IO "MIDNIGHT CINEMA" GLOBAL CSS ---
st.markdown("""
<style>
:root {
    --color-carbon-vellum: #fcfcfc;
    --color-obsidian: #0a0a13;
    --color-void: #040407;
    --color-graphite: #08080c;
    --color-smoke: #757580;
    --color-ash: #a3a3b3;
    --color-charcoal: #2a2a32;
    --color-iris-glow: #6199f6;
    --color-twilight: #4f4f80;
    
    --font-primary: 'Inter', ui-sans-serif, system-ui, sans-serif;
    --font-eyebrow: 'Space Mono', monospace;
    --radius-cards: 10px;
    --radius-pills: 100px;
}

/* Global Canvas */
.stApp {
    background-color: var(--color-obsidian);
    color: var(--color-carbon-vellum);
    font-family: var(--font-primary);
}

h1, h2, h3, h4 { 
    color: var(--color-carbon-vellum) !important; 
    font-weight: 400 !important; 
    letter-spacing: -1.5px !important; 
}

p, span, label, .stMarkdown { 
    color: var(--color-ash); 
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: var(--color-void) !important;
    border-right: 1px solid var(--color-charcoal);
}
[data-testid="stSidebar"] * {
    color: var(--color-carbon-vellum) !important;
}
[data-testid="stSidebar"] .stTextInput input {
    background-color: var(--color-void) !important;
    border: 1px solid var(--color-charcoal) !important;
    color: var(--color-carbon-vellum) !important;
    border-radius: var(--radius-cards) !important;
}
[data-testid="stSidebar"] .stTextInput input:focus {
    border-color: var(--color-iris-glow) !important;
    box-shadow: 0 0 8px rgba(97, 153, 246, 0.3) !important;
}

/* Buttons (Pill Geometry) */
.stButton > button {
    background-color: transparent !important;
    color: var(--color-carbon-vellum) !important;
    border: 1px solid var(--color-carbon-vellum) !important;
    border-radius: var(--radius-pills) !important;
    padding: 14px 28px !important;
    font-weight: 400 !important;
    width: 100%;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    background-color: var(--color-carbon-vellum) !important;
    color: var(--color-obsidian) !important;
}
.stButton > button[kind="primary"] {
    background-color: var(--color-carbon-vellum) !important;
    color: var(--color-obsidian) !important;
    border: none !important;
    font-weight: 500 !important;
}

/* Hero Card - Cosmic Gradient & Violet Halo */
.hero-card {
    background: linear-gradient(195deg, #0a0010 0%, #02000a 50%, #0c1d32 100%);
    border: 1px solid var(--color-twilight);
    border-radius: var(--radius-cards);
    padding: 4rem 2rem;
    text-align: center;
    box-shadow: inset 0 0 0 1px #4f4f80, 0 0 60px rgba(79, 79, 128, 0.15);
    margin-bottom: 2rem;
}
.hero-card h1 { font-size: 3.5rem !important; font-weight: 400 !important; margin: 0; letter-spacing: -2.5px !important; }
.hero-card p  { font-size: 1.1rem; color: var(--color-smoke); margin-top: 1rem; }

/* Eyebrow Label */
.eyebrow-label {
    font-family: var(--font-eyebrow);
    font-size: 12px;
    color: var(--color-iris-glow);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    line-height: 0.90;
    margin-bottom: 1rem;
}

/* Feature Grid - Transparent Typography Blocks */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
    margin-top: 1.5rem;
}
.feature-card {
    background-color: transparent;
    padding: 1.25rem;
    text-align: center;
}
.feature-card .icon { font-size: 2rem; margin-bottom: 1rem; color: var(--color-iris-glow); }
.feature-card h4 { font-size: 1.25rem; font-weight: 500 !important; color: var(--color-carbon-vellum); margin: 0; }
.feature-card p  { font-size: 0.95rem; color: var(--color-ash); margin: 0.5rem 0 0; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)

# Session state
for key, val in {"logged_in": False, "username": ""}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Sidebar
with st.sidebar:
    st.markdown("## 💼 AI Job Copilot")
    st.markdown("---")
    tab = st.radio("Authentication", ["Login", "Sign Up"], label_visibility="collapsed")
    st.markdown("")

    if tab == "Login":
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
                st.error("Invalid credentials.")

    else:
        st.markdown("**Create your account**")
        username = st.text_input("Username", placeholder="Choose a username", key="su_user")
        password = st.text_input("Password", type="password", placeholder="Choose a password", key="su_pass")
        if st.button("Create Account →", use_container_width=True):
            if create_user(username, password):
                st.success("Account created! Please login.")
            else:
                st.error("Username already exists.")

# Main hero
if not st.session_state.logged_in:
    st.markdown("""
    <div class="hero-card">
      <div class="eyebrow-label">THE COPILOT PLATFORM</div>
      <h1>AI Job Copilot</h1>
      <p>AI Resume Matcher · Skill Gap Detector · Career Coach</p>
    </div>
    
    <div class="feature-grid">
      <div class="feature-card">
          <div class="icon">📄</div>
          <h4>Resume Analysis</h4>
          <p>AI-powered insights tailored to your specific career trajectory.</p>
      </div>
      <div class="feature-card">
          <div class="icon">🎯</div>
          <h4>Job Matching</h4>
          <p>Semantic scoring to map your profile perfectly against the market.</p>
      </div>
      <div class="feature-card">
          <div class="icon">🗺️</div>
          <h4>30-Day Roadmap</h4>
          <p>Personalized step-by-step plans to conquer your skill gaps.</p>
      </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f'<div class="eyebrow-label">DASHBOARD</div>', unsafe_allow_html=True)
    st.markdown(f"<h1>Welcome back, {st.session_state.username}</h1>", unsafe_allow_html=True)
    st.write("Use the sidebar navigation to access your resume analysis and job matches.")
