# AI-Powered Recruitment Platform

Our AI-powered recruitment platform revolutionizes hiring by automating initial candidate screening, intelligently ranking resumes, and conducting voice-based adaptive interviews — all while keeping the recruiter in control through a **Human-in-the-Loop** design.

---

## 🚀 Key Features

### 🔍 Smart Resume Screening

- **Resume Retrieval**: Fetches candidate resumes from **Azure Cosmos DB**.
- **Similarity Scoring**: Computes semantic similarity between resumes and job descriptions using **OpenAI’s `text-embedding-ada-002`** model.
- **Candidate Ranking**: Uses **cosine similarity** to rank applicants and identify the most relevant profiles.
- **Effort Reduction**: Filters out irrelevant resumes, surfacing top candidates for recruiter review.

---

### 🎙️ Adaptive AI Interviews

Shortlisted candidates undergo a **voice-based AI interview** with the following capabilities:

- **Dynamic Questioning**: Questions adapt in real-time based on the candidate's spoken responses.
- **Topic Shifting & Difficulty Escalation**: Personalizes the interview experience to fairly assess both **technical** and **communication** skills.

---

### 📊 Post-Interview Insights

Generates detailed interview reports using multiple AI-powered tools:

- **Transcription**: Powered by **Azure Speech Services**.
- **Audio Analysis**: Uses **Librosa** to assess vocal features like **confidence**, **calmness**, and **expressiveness**.
- **LLM-Based Evaluation**: Scores candidates on **technical aptitude**, **clarity**, and **communication**.

These reports help recruiters make informed decisions and give high-potential candidates a fair shot — even if their resumes fall short.

---

## 🧭 Recruiter Co-Pilot

An intelligent assistant designed to empower recruiters with real-time support:

- **Vector Search**: Enables semantic candidate search using **Azure Cognitive Search + Cosmos DB** with embeddings from `text-embedding-ada-002`.
  
  Example query:  
  > “Find candidates with 3+ years in backend development with Node.js”

- **Prompt-Based Assistance**: Receive smart suggestions and best practices in real-time.
  
  Example prompts:  
  > “Suggest five screening questions for a frontend engineer”  
  > “What are common red flags in junior developer resumes?”

---

## 🛠️ Tech Stack

- **Azure AI services - LLMs**:`gpt-40` Interview evaluation and report generation and recruitment assistance,`text-embedding-ada-002`**: Text similarity and semantic search
- **Azure Cognitive Search**: Vector-powered candidate search
- **Azure Cosmos DB**: Resume data storage
- **Azure Speech Services SDK**: Voice transcription
- **Azure blob**: To store interview audios
- **Azure communication services**: To send emails to the relevant candidates
- **Librosa**: Interview audio analysis
- **FastAPI**:Backend development
- **ReactJS,Chakra UI**:FrontEnd development
- **Web Speech API**:Real time speech transcription
- **Vercel**:Frontend deployment
- **Railway**:Backend deployment

---

## ✅ Benefits

- Reduce recruiter workload through automation
- Ensure fair evaluation beyond resume content
- Deliver a personalized candidate experience
- Make informed, bias-reduced hiring decisions

---

## 📬 Contact

For inquiries, demos, or integrations, please reach out at [your-email@example.com].
