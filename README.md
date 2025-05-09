# AI-Powered Recruitment Platform

Our AI-powered recruitment platform revolutionizes hiring by automating initial candidate screening, intelligently ranking resumes, and conducting voice-based adaptive interviews — all while keeping the recruiter in control through a **Human-in-the-Loop** design.

---
## Why we chose to build it?
We chose to build TalentScout because hiring today is deeply inefficient and biased. Recruiters are overwhelmed with irrelevant resumes, while great candidates are filtered out early due to resource constraints. We wanted to create a system that levels the playing field — where AI handles the screening, interviews, and reporting, allowing recruiters to focus on what truly matters: decision-making and human connection. This solution not only solves a clear industry pain point, but also brings Responsible AI into real-world hiring processes.


## 🚀 Key Features

### 🔍 Smart Resume Screening

- **Resume Retrieval**: Fetches candidate resumes from **Azure Cosmos DB**.
- **Similarity Scoring**: Computes semantic similarity between resumes and job descriptions and and retrieves the top N candidates
- **Candidate Ranking**:Further using **OpenAI’s `text-embedding-ada-002`** LLM model the candidates are giving a ranking
- **Effort Reduction**: Filters out irrelevant resumes, surfacing top candidates for recruiter review.

---

### 🎙️ Adaptive AI Interviews

Shortlisted candidates undergo an **adaptive voice-based AI screening interview** with the following capabilities:
- **Voice based interview** Enables convenience and better expression
- **Topic relevance**: The AI Interviewer has the context of the candidate's profile and the job that they are interviewing for to ask the relevant questions
- **Dynamic Questioning**: Questions adapt in real-time based on the candidate's spoken responses.
- **Topic Shifting & Difficulty Escalation**: Personalizes the interview experience to fairly assess both **technical** and **communication** skills.

---

### 📊 Post-Interview Insights

Generates detailed interview reports using multiple AI-powered tools:

- **Transcription**: Powered by **Azure Speech Services**.
- **Audio Analysis**: Uses **Librosa** to assess vocal features like **confidence**, **calmness**, and **expressiveness**.
- **LLM-Based Evaluation**: Based on the Transcript and the audio analysis the AI agent Scores the candidates on **technical aptitude**, **clarity**, and **communication**.

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



| Technology                    | Purpose                                                                 |
|------------------------------|-------------------------------------------------------------------------|
| **Azure AI Services - LLMs** | `gpt-4o`: Interview evaluation, report generation, recruitment assistance  
|                              |`text-embedding-ada-002`: Text similarity and semantic search            |
| **Azure Cognitive Search**   | Vector-powered semantic candidate search                                |
| **Azure Cosmos DB**          | NoSQL database for storing candidates, jobs, and sessions               |
| **Azure Speech Services SDK**| Voice-to-text transcription of interview recordings                     |
| **Azure Blob Storage**       | Storage for audio files and media                                       |
| **Azure Communication Services** | Sending email communications to candidates                          |
|**Pydantic**                  | Type enforcement                                                        |
| **Librosa**                  | Audio feature extraction and analysis                                   |
| **FastAPI**                  | Backend development framework                                           |
| **ReactJS & Chakra UI**      | Frontend development with responsive, accessible UI                     |
| **Web Speech API**           | Real-time speech transcription in the browser                           |
| **Vercel**                   | Frontend hosting and deployment                                         |
| **Railway**                  | Backend deployment and infrastructure                                   |

---

![alt text](https://github.com/kruthikakalmali/TalentScout/blob/main/Architecture_diagrams/interview_flow.png)



![alt text](https://github.com/kruthikakalmali/TalentScout/blob/main/Architecture_diagrams/recruiter_copilot.png)



![alt text](https://github.com/kruthikakalmali/TalentScout/blob/main/Architecture_diagrams/jd_to_resume_matching.png)


## ✅ Benefits

- Reduce recruiter workload through automation
- Ensure fair evaluation beyond resume content
- Deliver a personalized candidate experience
- Make informed, bias-reduced hiring decisions

---

## Steps to run the code
# Fastapi Backend

```pip install -r requirements.txt```

```uvicorn app:app --reload```

# Reactjs frontend

```npm install```

```npm start```



## 📬 Contact

For inquiries, demos, or integrations, please reach out at [kruthikakalmali@gmail.com],[kunalmodi123@gmail.com].
