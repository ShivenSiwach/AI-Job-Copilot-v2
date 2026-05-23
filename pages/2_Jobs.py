import streamlit as st
from concurrent.futures import ThreadPoolExecutor
from agents import (
    search_agent, resume_agent, skill_gap_agent,
    learning_roadmap_agent, get_embedding, cosine_similarity
)

st.set_page_config(page_title="Jobs | AI Job Copilot", page_icon="", layout="wide")

if not st.session_state.get("logged_in"):
    st.warning(" Please login first."); st.stop()

st.markdown("""
<style>
.query-bar {
    background: #f8fafc; border-radius: 12px;
    padding: 1.5rem; margin-bottom: 1.5rem;
    border: 1px solid #e2e8f0;
}
.score-card {
    background: linear-gradient(135deg,#667eea,#764ba2);
    border-radius: 16px; padding: 1.5rem 2rem;
    color: white; display: flex;
    justify-content: space-between; align-items: center;
    margin-bottom: 1.5rem;
}
.score-card h2 { margin:0; font-size:2.5rem; font-weight:800; }
.score-card p  { margin:0; opacity:0.85; font-size:0.9rem; }
.badge {
    display: inline-block; padding: 4px 12px;
    border-radius: 20px; font-size: 0.75rem; font-weight: 600;
}
.badge-green  { background:#dcfce7; color:#166534; }
.badge-yellow { background:#fef9c3; color:#854d0e; }
.badge-red    { background:#fee2e2; color:#991b1b; }
.example-chip {
    display: inline-block; background:#ede9fe; color:#6d28d9;
    border-radius:20px; padding:4px 12px; font-size:0.75rem;
    margin:3px; cursor:pointer;
}
</style>
""", unsafe_allow_html=True)

st.title(" AI Job Recommendations")

#  Sidebar query input
with st.sidebar:
    st.markdown("###  Job Search Settings")
    job_query = st.text_input("Enter job query", placeholder="e.g. Entry level Data Scientist")
    st.markdown("**Example queries:**")
    for q in ["Data Analyst with SQL", "ML Intern", "Junior Data Scientist", "Data Scientist Fresher"]:
        st.markdown(f'<span class="example-chip">{q}</span>', unsafe_allow_html=True)

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
        f_skill   = ex.submit(skill_gap_agent,        resume, jobs)
        f_roadmap = ex.submit(learning_roadmap_agent, resume, jobs)

    progress.progress(75, text="Calculating match score...")
    job_emb = get_embedding(jobs)
    res_emb = get_embedding(resume)
    score   = cosine_similarity(job_emb, res_emb)
    pct     = round(score * 100, 2)
    progress.progress(100, text="Done!")

    #  Score card 
    badge = ("badge-green", "Excellent match") if pct >= 80 else \
            ("badge-yellow", "Good match")    if pct >= 60 else \
            ("badge-red", "Needs improvement")
    st.markdown(f"""
    <div class="score-card">
      <div>
        <p>Resume–Job Match Score</p>
        <h2>{pct}%</h2>
        <span class="badge {badge[0]}">{badge[1]}</span>
      </div>
      <div style="font-size:3rem"></div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(score)

    #  Result tabs 
    t1,t2,t3,t4 = st.tabs([" Jobs Found"," Resume Analysis"," Skill Gap"," 30-Day Roadmap"])
    with t1: st.markdown(jobs)
    with t2: st.markdown(f_resume.result())
    with t3: st.markdown(f_skill.result())
    with t4: st.markdown(f_roadmap.result())