import os
import time
from dotenv import load_dotenv
import numpy as np

# Safe import for the GenAI SDK
try:
    import google.genai as genai
except Exception:
    genai = None

# Load .env file for local development
load_dotenv()

def _get_api_key() -> str | None:
    # 1. Priority: Try Streamlit secrets (for cloud deployment)
    try:
        import streamlit as st
        secrets = st.secrets
        if "GOOGLE_API_KEY" in secrets:
            return secrets["GOOGLE_API_KEY"]
    except Exception:
        pass

    # 2. Fallback: Try local environment variable (for local development)
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        return api_key

    return None

# Initialize Client
API_KEY = _get_api_key()
if API_KEY and genai is not None:
    client = genai.Client(api_key=API_KEY)
else:
    client = None

MODEL = "gemini-3.1-flash-lite"

def generate_with_retry(prompt: str, retries: int = 3) -> str:
    if client is None:
        return "AI features are unavailable because the Google API key is not configured."

    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            if attempt < retries - 1:  # Don't sleep on the last attempt
                time.sleep(2)
    return "Model unavailable. Please try again."

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
    """
    Get embedding for text using Google's embedding models.
    """
    if client is None:
        return np.zeros(1, dtype=float)

    # Ensure text is a string
    if not isinstance(text, str):
        text = str(text)
    
    # Prioritize text-embedding-004 over legacy models
    embedding_models = [
        "text-embedding-004", 
        "embedding-001",        
        "gemini-embedding-001" 
    ]
    
    for model_name in embedding_models:
        try:
            result = client.models.embed_content(
                model=model_name,
                contents=[text]
            )
            if hasattr(result, 'embeddings') and len(result.embeddings) > 0:
                return np.array(result.embeddings[0].values)
            if hasattr(result, 'embedding'):
                return np.array(result.embedding)
        except Exception as e:
            error_str = str(e).lower()
            print(f"Embedding failed with model {model_name}: {e}")
            
            # If the API key is unauthorized or invalid, stop and raise the error immediately
            if any(err in error_str for err in ["401", "400", "unauthenticated", "invalid_argument"]):
                raise RuntimeError("Authentication failed. Please check your GOOGLE_API_KEY settings.")
            
            # If the model is simply not found (404), fall back to the next one
            if "not found" in error_str or "not_found" in error_str or "404" in error_str:
                continue

    # Return empty array if all models fail (prevents full app crash)
    print("All embedding models failed.")
    return np.zeros(1, dtype=float)

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))
