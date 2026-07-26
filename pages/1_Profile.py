import streamlit as st
import sqlite3
from pypdf import PdfReader

st.set_page_config(page_title="Profile | AI Job Copilot", layout="wide")

# Ensure CSS persists
def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass # Handle if running from different directory
load_css("style.css") 
load_css("../style.css")

if 'username' not in st.session_state or st.session_state.username is None:
    st.warning("Session expired. Please log in from the main app page.")
    st.stop() 

conn   = sqlite3.connect("data/users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("SELECT * FROM user_profiles WHERE username=?", (st.session_state.username,))
profile = cursor.fetchone()

st.markdown("""
<style>
.profile-header {
    display: flex; align-items: center; gap: 1.5rem;
    padding: 2rem; background: var(--color-graphite);
    border-radius: var(--radius-cards); margin-bottom: 2rem;
    border: 1px solid var(--color-twilight);
    box-shadow: inset 0 0 0 1px #4f4f80, 0 0 60px rgba(79, 79, 128, 0.15);
}
.avatar {
    width: 64px; height: 64px; border-radius: 50%;
    background: var(--color-iris-glow);
    display: flex; align-items: center; justify-content: center;
    color: var(--color-obsidian); font-size: 1.5rem; font-weight: 600; flex-shrink: 0;
}
.profile-header h2 { margin: 0 !important; font-size: 1.5rem !important; color: var(--color-carbon-vellum); font-weight: 500 !important; letter-spacing: -1px; }
.profile-header p  { margin: 0; font-size: 0.95rem; color: var(--color-ash); }
.upload-zone {
    border: 1px dashed var(--color-iris-glow); border-radius: var(--radius-cards);
    padding: 3rem; text-align: center; background: rgba(97, 153, 246, 0.05);
}
.upload-zone p { color: var(--color-iris-glow); margin: 0.5rem 0 0; font-size: 0.85rem; font-weight: 500;}
</style>
""", unsafe_allow_html=True)

initials = st.session_state.username[:2].upper()
st.markdown('<div class="eyebrow-label">USER PROFILE</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="profile-header">
  <div class="avatar">{initials}</div>
  <div>
    <h2>{st.session_state.username}</h2>
    <p>Career profile & resume</p>
  </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Profile Info", "Resume"])

with tab1:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        education  = st.text_input("Education",  value=profile[1] if profile else "", placeholder="e.g. B.Tech Computer Science")
        role       = st.text_input("Preferred Role", value=profile[4] if profile else "", placeholder="e.g. Machine Learning Engineer")
    with col2:
        location   = st.text_input("Location",   value=profile[5] if profile else "", placeholder="e.g. Stockholm, Sweden")
        skills     = st.text_area("Skills",      value=profile[2] if profile else "", placeholder="Python, SQL, ML...", height=100)
        
    experience = st.text_area("Experience", value=profile[3] if profile else "", placeholder="Describe your experience...", height=120)

    if st.button("Save Profile", use_container_width=True):
        cursor.execute(
            "INSERT OR REPLACE INTO user_profiles VALUES (?,?,?,?,?,?)",
            (st.session_state.username, education, skills, experience, role, location)
        )
        conn.commit()
        st.success("✅ Profile saved successfully!")
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<div class="upload-zone">', unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload your resume", type=["pdf"], label_visibility="collapsed")
    st.markdown('<p>Drop your PDF resume here · Max 200MB</p></div>', unsafe_allow_html=True)

    if uploaded:
        text = ""
        for page in PdfReader(uploaded).pages:
            if page.extract_text():
                text += page.extract_text()
        st.session_state.resume_text = text
        st.success("✅ Resume extracted successfully!")
        with st.expander("Preview extracted text"):
            st.text(text[:1500] + "..." if len(text) > 1500 else text)
    st.markdown('</div>', unsafe_allow_html=True)
