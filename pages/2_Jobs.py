import streamlit as st
from concurrent.futures import ThreadPoolExecutor
from agents import (
    search_agent, resume_agent, skill_gap_agent,
    learning_roadmap_agent, get_embedding, cosine_similarity
)

st.set_page_config(page_title="Jobs | AI Job Copilot", layout="wide")

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

# --- Page Header ---
st.title("Job Matching")
st.tabs(["Recommendations", "Saved Jobs", "Application History"])

# --- Split Layout ---
left_col, right_col = st.columns([2.5, 1.5])

# LEFT COLUMN: The Job Inputs & Results
with left_col:
    st.markdown('<div class="dash-card">', unsafe_allow_html=True)
    st.markdown("<h4>Search Settings</h4>", unsafe_allow_html=True)
    job_query = st.text_input("Enter job query", placeholder="e.g. Entry level Data Scientist", label_visibility="collapsed")
    
    resume = st.session_state.get("resume_text", "")
    
    if st.button("✨ 1-click analysis", type="primary"):
        if not resume:
            st.error("Please upload your resume on the Profile page first.")
        else:
            progress = st.progress(0, text="Searching for matching jobs...")
            jobs = search_agent(job_query)
            
            progress.progress(25, text="Analysing resume...")
            with ThreadPoolExecutor() as ex:
                f_resume  = ex.submit(resume_agent, resume)
                f_skill   = ex.submit(skill_gap_agent, resume, jobs)
                f_roadmap = ex.submit(learning_roadmap_agent, resume, jobs)

            progress.progress(75, text="Calculating match score...")
            job_emb = get_embedding(jobs)
            res_emb = get_embedding(resume)
            score   = cosine_similarity(job_emb, res_emb)
            pct     = round(score * 100, 2)
            progress.progress(100, text="Done!")

            st.session_state['ai_jobs'] = jobs
            st.session_state['ai_resume'] = f_resume.result()
            st.session_state['ai_skill'] = f_skill.result()
            st.session_state['ai_roadmap'] = f_roadmap.result()
            st.session_state['analysis_complete'] = True
            st.session_state['latest_pct'] = pct

            st.success("Analysis Complete!")
    st.markdown('</div>', unsafe_allow_html=True)

    # Display Jobs if they exist
    if st.session_state.get('analysis_complete'):
        st.markdown('<div class="dash-card">', unsafe_allow_html=True)
        st.markdown("<h4>Matched Roles</h4>", unsafe_allow_html=True)
        st.markdown(st.session_state['ai_jobs'])
        st.markdown('</div>', unsafe_allow_html=True)

# RIGHT COLUMN: Metrics & Actions
with right_col:
    # Match Score Metric
    st.markdown('<div class="dash-card">', unsafe_allow_html=True)
    st.markdown("<h4>Current Match Score</h4>", unsafe_allow_html=True)
    pct_val = st.session_state.get('latest_pct', 0)
    st.metric(label="Resume Fit", value=f"{pct_val}%", delta="Ready to apply" if pct_val > 75 else "Needs improvement")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Actions List
    st.markdown('<div class="dash-card">', unsafe_allow_html=True)
    st.markdown("<h4>Quick Actions</h4>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="list-item">
        <div><h4>Profile Settings</h4><p>Update your resume</p></div>
    </div>
    <div class="list-item">
        <div><h4>Skill Gap</h4><p>View missing skills</p></div>
    </div>
    <div class="list-item" style="border-bottom: none;">
        <div><h4>Roadmap</h4><p>View 30-day plan</p></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
