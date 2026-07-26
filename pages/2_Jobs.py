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

st.markdown('<div class="eyebrow-label">JOB MATCHING ENGINE</div>', unsafe_allow_html=True)
st.title("AI Job Recommendations")

# Sidebar query input
with st.sidebar:
    st.markdown("### Job Search Settings")
    job_query = st.text_input("Enter job query", placeholder="e.g. Entry level Data Scientist")
    st.markdown("**Example queries:**")
    st.markdown("Data Analyst with SQL • ML Intern • Junior Data Scientist")

resume = st.session_state.get("resume_text", "")

if not resume:
    st.info("Please upload your resume on the **Profile** page first.")
    st.stop()

if st.button("Analyse Resume & Find Jobs", use_container_width=True):
    progress = st.progress(0, text="Searching for matching jobs...")
    jobs = search_agent(job_query)
    
    progress.progress(25, text="Analysing resume...")
    with ThreadPoolExecutor() as ex:
        f_resume  = ex.submit(resume_agent,          resume)
        f_skill   = ex.submit(skill_gap_agent,       resume, jobs)
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

    st.success("✅ Analysis Complete! Use the sidebar to view detailed results.")
    
    st.markdown(f"""
    <div class="custom-card" style="text-align: center; border-color: var(--color-iris-glow);">
        <h2 style="color: var(--color-iris-glow) !important; margin: 0; font-size: 3rem !important;">{pct}%</h2>
        <p style="color: var(--color-carbon-vellum); font-size: 1.2rem;">Resume Match Score</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Jobs Found")
    st.markdown(f'<div class="custom-card">{jobs}</div>', unsafe_allow_html=True)
