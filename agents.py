import os, time
from dotenv import load_dotenv
import numpy as np
import google.genai as genai

# Load .env file
load_dotenv()

# Configure API key with validation
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable is not set")

# Initialize the client with API key
client = genai.Client(api_key=api_key)
MODEL = "gemini-3.1-flash-lite"

def generate_with_retry(prompt: str, retries: int = 3) -> str:
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
    Note: Model names may change over time. Current models to try:
    - embedding-001 (recommended)
    - text-embedding-004
    - gemini-embedding-001
    """
    # Ensure text is a string
    if not isinstance(text, str):
        text = str(text)
    
    # List of embedding models to try, in order of preference
    embedding_models = [
        "embedding-001",        # Current recommended model
        "text-embedding-004",  # Previous generation
        "gemini-embedding-001" # Legacy model
    ]
    
    for model_name in embedding_models:
        try:
            result = client.models.embed_content(
                model=model_name,
                contents=[text]
            )
            # Extract the embedding values
            if hasattr(result, 'embeddings') and len(result.embeddings) > 0:
                return np.array(result.embeddings[0].values)
            else:
                # Try alternative response structure
                if hasattr(result, 'embedding'):
                    return np.array(result.embedding)
        except Exception as e:
            # Only continue if it's a model not found error
            error_str = str(e).lower()
            if "not found" in error_str or "not_found" in error_str or "404" in error_str:
                continue
            else:
                # For other errors (like auth issues), re-raise with context
                raise RuntimeError(f"Embedding failed with model {model_name}: {e}")
    
    raise RuntimeError(
        "No working embedding model found. "
        "Please check: 1) Your API key is valid, 2) Your account has access to embedding models, "
        "3) The model names haven't changed. "
        "Try updating the embedding_models list in get_embedding() function."
    )

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))