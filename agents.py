import os, time
import numpy as np
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL = "gemini-2.5-flash"

def generate_with_retry(prompt: str, retries: int = 3) -> str:
    for attempt in range(retries):
        try:
            model    = genai.GenerativeModel(MODEL)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(2)
    return " Model unavailable. Please try again."

def search_agent(query: str) -> str:
    return generate_with_retry(f"""
Find 3 realistic Data Science / Machine Learning jobs in India for:
{query}

For each job include:
**Job Title** | Company | Location
Required Skills (bullet list)
Experience Level | Salary Range (if known)
2-line job description
---
""")

def resume_agent(resume_text: str) -> str:
    return generate_with_retry(f"""
Analyse this resume as an expert recruiter. Provide:
1. **Key Technical Skills** – grouped by category
2. **Experience Level** – with justification
3. **Strengths** – top 3 with examples from the resume
4. **Missing Skills** – critical gaps for modern roles
5. **Overall Feedback** – 3–4 sentences, constructive and specific

Resume:
{resume_text}
""")

def skill_gap_agent(resume_text: str, jobs: str) -> str:
    return generate_with_retry(f"""
Compare the resume against the job descriptions. Provide:
1. **Matching Skills** – what already aligns well
2. **Missing Skills** – ranked by importance
3. **Missing Tools/Technologies** – specific software gaps
4. **Priority Actions** – top 5 things to do first

RESUME:
{resume_text}

JOBS:
{jobs}
""")

def learning_roadmap_agent(resume_text: str, jobs: str) -> str:
    return generate_with_retry(f"""
Create a practical 30-day learning roadmap. Format as:

**Week 1 (Days 1–7): Foundation**
- What to learn, why it matters, daily time (~2–3 hrs)

**Week 2 (Days 8–14): Core Skills**
...

**Week 3 (Days 15–21): Applied Practice**
...

**Week 4 (Days 22–30): Portfolio & Polish**
...

End with: Resume update checklist + 3 project ideas.

RESUME: {resume_text}
JOBS: {jobs}
""")

def get_embedding(text: str) -> np.ndarray:
    result = genai.embed_content(
        model="models/gemini-embedding-001",
        content=text,
        task_type="retrieval_document"
    )
    return np.array(result["embedding"])

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))