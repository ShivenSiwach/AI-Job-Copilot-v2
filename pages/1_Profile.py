import streamlit as st
import sqlite3
from pypdf import PdfReader

st.set_page_config(page_title="Profile | AI Job Copilot", layout="wide")

# 1. CONNECT TO THE DATABASE FIRST
conn   = sqlite3.connect("data/users.db", check_same_thread=False)
cursor = conn.cursor()

# 2. FETCH THE PROFILE ONCE
cursor.execute("SELECT * FROM profiles WHERE username=?", (st.session_state.username,))
profile = cursor.fetchone()

# 3. APPLY CSS STYLING
st.markdown("""
<style>
.profile-header {
    display: flex; align-items: center; gap: 1rem;
    padding: 1.5rem; background: #f8fafc;
    border-radius: 12px; margin-bottom: 1.5rem;
    border: 1px solid #e2e8f0;
}
.avatar {
    width: 56px; height: 56px; border-radius: 50%;
    background: linear-gradient(135deg,#6366f1,#8b5cf6);
    display: flex; align-items: center; justify-content: center;
    color: white; font-size: 1.4rem; font-weight: 700; flex-shrink: 0;
}
.profile-header h2 { margin: 0; font-size: 1.2rem; color: #1e293b; }
.profile-header p  { margin: 0; font-size: 0.85rem; color: #64748b; }
.section-card {
    border: 1px solid #e2e8f0; border-radius: 12px;
    padding: 1.5rem; margin-bottom: 1rem; background: white;
}
.section-card h4 { margin: 0 0 1rem; font-size: 0.95rem; color: #374151; }
.upload-zone {
    border: 2px dashed #c7d2fe; border-radius: 12px;
    padding: 2rem; text-align: center; background: #f5f3ff;
}
.upload-zone p { color: #6366f1; margin: 0.5rem 0 0; font-size: 0.85rem; }
.save-btn > button {
    background: #6366f1 !important; color: white !important;
    border-radius: 8px !important; font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# 4. RENDER HEADER
initials = st.session_state.username[:2].upper()
st.markdown(f"""
<div class="profile-header">
  <div class="avatar">{initials}</div>
  <div>
    <h2>{st.session_state.username}</h2>
    <p>Career profile & resume</p>
  </div>
</div>
""", unsafe_allow_html=True)

# 5. RENDER TABS
tab1, tab2 = st.tabs([" Profile Info", " Resume"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        # The 'if profile else' logic safely handles new users with empty DB rows
        education  = st.text_input(" Education",  value=profile[1] if profile else "", placeholder="e.g. B.Tech Computer Science")
        role       = st.text_input(" Preferred Role", value=profile[4] if profile else "", placeholder="e.g. Machine Learning Engineer")
    with col2:
        location   = st.text_input(" Location",   value=profile[5] if profile else "", placeholder="e.g. Stockholm, Sweden")
        skills     = st.text_area(" Skills",      value=profile[2] if profile else "", placeholder="Python, SQL, ML...", height=100)
        
    experience = st.text_area(" Experience", value=profile[3] if profile else "", placeholder="Describe your experience...", height=120)

    if st.button(" Save Profile", use_container_width=True):
        cursor.execute(
            "INSERT OR REPLACE INTO profiles VALUES (?,?,?,?,?,?)",
            (st.session_state.username, education, skills, experience, role, location)
        )
        conn.commit()
        st.success(" Profile saved successfully!")

with tab2:
    st.markdown('<div class="upload-zone">', unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload your resume", type=["pdf"], label_visibility="collapsed")
    st.markdown('<p> Drop your PDF resume here · Max 200MB</p></div>', unsafe_allow_html=True)

    if uploaded:
        text = ""
        for page in PdfReader(uploaded).pages:
            if page.extract_text():
                text += page.extract_text()
        st.session_state.resume_text = text
        st.success(" Resume extracted successfully!")
        with st.expander(" Preview extracted text"):
            st.text(text[:1500] + "..." if len(text) > 1500 else text)
