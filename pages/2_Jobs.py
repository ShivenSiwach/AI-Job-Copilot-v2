import streamlit as st
from concurrent.futures import ThreadPoolExecutor
from agents import (
    search_agent, resume_agent, skill_gap_agent,
    learning_roadmap_agent, get_embedding, cosine_similarity
)

st.set_page_config(page_title="Jobs | AI Job Copilot", layout="wide")

if not st.session_state.get("logged_in"):
    st.warning(" Please login first."); st.stop()

st.title(" AI Job Recommendations")

# Sidebar query input
with st.sidebar:
    st.markdown("###  Job Search Settings")
    job_query = st.text_input("Enter job query", placeholder="e.g. Entry level Data Scientist")
    st.markdown("**Example queries:**")
    st.markdown("Data Analyst with SQL • ML Intern • Junior Data Scientist")

resume = st.session_state.get("resume_text", "")

if not resume:
    st.info(" Please upload your resume on the **Profile** page first.")
    st.stop()

if st.button(" Analyse Resume & Find Jobs", use_container_width=True):
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

    # --- THE FIX: SAVE EVERYTHING TO SESSION STATE ---
    st.session_state['ai_jobs'] = jobs
    st.session_state['ai_resume'] = f_resume.result()
    st.session_state['ai_skill'] = f_skill.result()
    st.session_state['ai_roadmap'] = f_roadmap.result()
    st.session_state['analysis_complete'] = True
    # -------------------------------------------------

    st.success("Analysis Complete! Use the sidebar to view your results.")
    st.markdown(f"**Resume–Job Match Score:** {pct}%")
    st.markdown("### Jobs Found")
    st.markdown(jobs) # Display jobs here as the starting point
