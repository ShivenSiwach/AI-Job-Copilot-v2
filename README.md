#  AI Job Copilot v2
### Agentic AI Resume Matcher & Job Recommender

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.45.1-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/Google%20Gemini-API-4285F4?style=for-the-badge&logo=google&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

> An intelligent career guidance system that analyzes your resume, recommends job roles, detects skill gaps, and generates a personalized 30-day learning roadmap — powered by LLMs, semantic embeddings, and cosine similarity.

---

##  Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [How It Works](#-how-it-works)
- [Screenshots](#-screenshots)
- [Match Score Interpretation](#-match-score-interpretation)
- [Future Scope](#-future-scope)
- [Contributing](#-contributing)
- [License](#-license)

---

##  Overview

**AI Job Copilot v2** is an end-to-end intelligent career assistance platform built for students, fresh graduates, and early-career professionals. It bridges the gap between academic skills and industry expectations by combining:

-  **Secure user authentication** with bcrypt-hashed passwords
-  **AI-powered resume analysis** via Google Gemini API
-  **Semantic job matching** using embeddings and cosine similarity
-  **Personalized 30-day learning roadmaps**
-  **Persistent user profiles** backed by SQLite

Unlike keyword-based resume screeners, v2 understands the *context* of your experience and measures how closely your profile aligns with real industry requirements.

---

##  Features

###  User Authentication
- Secure login and signup with session management
- Passwords hashed using **bcrypt** — never stored in plain text
- Session state maintained across all Streamlit pages

###  Persistent User Profiles
- Save education, skills, experience, preferred role, and location
- Data persists in **SQLite** across sessions — no re-entry needed
- Upload your resume once and reuse it every visit

###  Resume Upload & Parsing
- Upload resume in **PDF format**
- Automatic text extraction using **PyPDF**
- Extracted content previewed and passed to AI agents

###  AI Job Recommendations
- Enter a job query (e.g., *"Junior Data Scientist with Python"*)
- Generates 3 realistic, India-based job descriptions with title, company, skills, and experience level

###  Resume Analysis
- Extracts key technical skills, strengths, and experience level
- Identifies missing skills and provides recruiter-style feedback

###  Skill Gap Detection
- Compares your resume against generated job requirements
- Lists matching skills, missing skills, missing tools, and improvement priorities

###  30-Day Learning Roadmap
- Structured week-by-week learning plan
- Suggests specific projects to build and interview prep tips

###  Semantic Match Score
- Converts resume and job descriptions into **embedding vectors**
- Computes **cosine similarity** for a contextual match percentage
- Goes beyond keyword matching to evaluate deeper relevance

---

##  System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     INPUT LAYER                         │
│        Login/Signup · Profile · Resume PDF · Query      │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│           AUTHENTICATION & SESSION LAYER                 │
│         bcrypt Verification · session_state             │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│                   DATABASE LAYER                         │
│         SQLite (users.db) · users · profiles            │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│               DATA PROCESSING LAYER                      │
│          PyPDF Text Extraction · Session State          │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│                  AI AGENT LAYER                          │
│   Job Search · Resume Analysis · Skill Gap · Roadmap    │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│               SEMANTIC MATCHING LAYER                    │
│       Gemini Embeddings · Cosine Similarity · Score     │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│              OUTPUT LAYER (Streamlit UI)                 │
│     Jobs · Resume Analysis · Skill Gap · Roadmap        │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Technology | Role | Version |
|---|---|---|
| Python | Core language | 3.10+ |
| Streamlit | Multi-page web UI | 1.45.1 |
| Google Gemini API | LLM — analysis, generation, embeddings | gemini-1.5-flash |
| PyPDF | PDF resume text extraction | 5.5.0 |
| NumPy | Vector operations & similarity computation | 2.2.5 |
| scikit-learn | ML utilities | 1.6.1 |
| SQLite (sqlite3) | Persistent user data storage | Built-in |
| bcrypt | Password hashing & verification | 4.3.0 |
| python-dotenv | Secure API key management | 1.0.1 |

---

##  Project Structure

```
AI_JOB_COPILOT/
│
├── app.py                   # Main entry point — Login / Signup UI
├── agents.py                # All AI agent logic (job search, analysis, embeddings)
├── auth.py                  # User registration and login logic
├── database.py              # SQLite schema creation and initialization
│
├── pages/
│   ├── 1_Profile.py         # User dashboard and resume upload
│   ├── 2_Jobs.py            # AI analysis trigger and results display
│   ├── 3_Resume_Analysis.py # Resume insights page
│   ├── 4_Skill_Gap.py       # Skill gap report page
│   └── 5_Roadmap.py         # 30-day learning roadmap page
│
├── data/
│   └── users.db             # SQLite database (auto-created on first run)
│
├── requirements.txt         # Python dependencies
├── .env                     # API key (not committed to version control)
├── .gitignore
└── README.md
```

---

##  Installation

### 1. Clone the repository

```bash
git clone https://github.com/ShivenSiwach/AI-Job-Copilot-v2.git
cd ai-job-copilot
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt**
```
streamlit==1.45.1
google-generativeai==0.8.5
numpy==2.2.5
pypdf==5.5.0
python-dotenv==1.0.1
scikit-learn==1.6.1
bcrypt==4.3.0
```

### 4. Initialize the database

```bash
python database.py
```

### 5. Launch the application

```bash
python -m streamlit run app.py
```

---

## 🔧 Configuration

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

> **How to get a Gemini API key:**
> 1. Go to [Google AI Studio](https://aistudio.google.com/)
> 2. Sign in with your Google account
> 3. Click **"Get API Key"** → **"Create API key"**
> 4. Copy the key and paste it in your `.env` file

> ⚠️ Never commit your `.env` file to version control. It is already listed in `.gitignore`.

---

## 🚀 Usage

### Step-by-step workflow

```
1. Open the app  →  app.py loads the Login / Signup page
2. Sign Up       →  Create an account (bcrypt-hashed password stored)
3. Log In        →  Authenticate and access the dashboard
4. Profile Page  →  Fill in your education, skills, experience, and upload your PDF resume
5. Jobs Page     →  Enter a job query (e.g., "Data Analyst with SQL and Power BI")
6. Click Analyze →  AI pipeline runs (job search + resume analysis + skill gap + roadmap)
7. View Results  →  Browse tabs: Jobs Found · Resume Analysis · Skill Gap · 30-Day Roadmap
```

### Example job queries

```
Data Analyst with SQL and Power BI
Junior Data Scientist
Machine Learning Intern
Data Scientist Fresher
Entry Level NLP Engineer
```

---

## ⚙️ How It Works

### AI Agent Pipeline

All four agents run via `agents.py` using the **Google Gemini API** (`gemini-1.5-flash`). Three agents execute **in parallel** using `ThreadPoolExecutor` to reduce wait time.

```python
with ThreadPoolExecutor() as executor:
    future_resume  = executor.submit(resume_agent,   resume)
    future_skill   = executor.submit(skill_gap_agent, resume, jobs)
    future_roadmap = executor.submit(learning_roadmap_agent, resume, jobs)
```

### Semantic Match Score

```
Resume Text  ──► Gemini Embedding ──► Vector A ──┐
                                                  ├──► Cosine Similarity ──► Match %
Job Descriptions ──► Gemini Embedding ──► Vector B ──┘
```

**Formula:**
```
Cosine Similarity(A, B) = (A · B) / (‖A‖ × ‖B‖)
```

### Password Security

```python
# Registration — hash before storing
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Login — verify without exposing raw password
bcrypt.checkpw(password.encode('utf-8'), stored_hash)
```

---

## 📸 Screenshots

| Page | Description |
|---|---|
| **Login / Signup** | Secure entry with sidebar menu |
| **Profile Dashboard** | Pre-filled fields, PDF upload, Save Profile |
| **Job Query Input** | Text input with example query suggestions |
| **Jobs Found Tab** | 3 realistic job descriptions with company and skills |
| **Match Score** | Semantic percentage score with progress bar |
| **Resume Analysis** | Skills, strengths, experience level, recruiter feedback |
| **Skill Gap Report** | Matching vs missing skills, tool gaps, priorities |
| **30-Day Roadmap** | Weekly plans, project suggestions, interview tips |

---

## 🎯 Match Score Interpretation

| Score | Label | Meaning |
|---|---|---|
| **80% and above** | 🟢 Excellent Match | Profile strongly aligns with the target role |
| **60% – 79%** | 🟡 Good Match | Some improvements can increase alignment |
| **Below 60%** | 🔴 Needs Improvement | Significant skill gaps to address |

---

## 🔮 Future Scope

- [ ] **Real-time job portal integration** — fetch live listings from LinkedIn, Naukri, or Indeed via APIs
- [ ] **JD Upload feature** — let users upload an actual job description for precise comparison
- [ ] **ATS Score System** — evaluate resume formatting, keyword density, and structure
- [ ] **AI-powered resume rewriting** — automated bullet point and wording improvements
- [ ] **Multi-role recommendation** — suggest alternative career paths from the same resume
- [ ] **RAG with vector databases** — integrate FAISS or Pinecone for contextual retrieval
- [ ] **Cloud deployment** — migrate from SQLite to PostgreSQL/Firebase for multi-user support
- [ ] **Email notifications** — job match alerts and roadmap reminders
- [ ] **Resume version control** — compare match scores across resume versions
- [ ] **Mobile-responsive UI** — improved Streamlit layout for smartphones and tablets

---

## 🤝 Contributing

Contributions are welcome! To get started:

```bash
# Fork the repo and create a feature branch
git checkout -b feature/your-feature-name

# Make your changes, then commit
git commit -m "feat: add your feature description"

# Push and open a Pull Request
git push origin feature/your-feature-name
```

Please follow the existing code structure — one agent per function, one feature per page.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

Built as an academic project demonstrating the application of **LLMs**, **NLP**, **semantic search**, and **AI-driven career guidance** in the HR-Tech / Career-Tech domain.

---

<div align="center">

⭐ **If this project helped you, give it a star!** ⭐

*AI Job Copilot v2 — Bridging the gap between academic learning and industry expectations*

</div>