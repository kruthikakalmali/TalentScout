

from fastapi import FastAPI, UploadFile, Form, File,HTTPException,Query
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import tempfile
from azure.storage.blob import BlobServiceClient
import uuid
from openai import AzureOpenAI,AsyncAzureOpenAI
import os
import librosa
import numpy as np
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from pydantic import BaseModel
import azure.cosmos
class AnalyzeRequest(BaseModel):
    session_id: str
from azure.cosmos import CosmosClient,PartitionKey
from pdfutility import extract_text_from_pdf
from downloadaudiofromazure import download_audio_from_azure
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add CORS middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Allow React app's URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)



AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
AZURE_CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
connect_str = os.getenv("AZURE_CONNECTION_STRING")
container_name = os.getenv("AZURE_CONTAINER_NAME")
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_client = blob_service_client.get_container_client(container_name)



from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
import uuid
# from azure.cosmos import CosmosClient, PartitionKey
import openai  # Azure OpenAI
import os

# Cosmos DB settings
COSMOS_ENDPOINT = "https://talentscoutdbfordata.documents.azure.com:443/"
COSMOS_KEY = "PKOeZAhLhViRqto2vXGTs6uabXAbOh0xRGjKdxvIkNovvJ6ZNqMnkUmFbm5XTTa9buCbBTuvo2zbACDbtRqVQQ=="
DATABASE_NAME = "talentscoutdatadb"
CONTAINER_NAME = "jobs"

# Azure OpenAI settings
# AZURE_OPENAI_ENDPOINT = "https://<your-openai-endpoint>.openai.azure.com/"
# AZURE_OPENAI_KEY = "<your-openai-key>"
AZURE_DEPLOYMENT_NAME = "gpt-4o"
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")

# Initialize Cosmos client
client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
database = client.create_database_if_not_exists(id=DATABASE_NAME)
container = database.create_container_if_not_exists(
    id=CONTAINER_NAME, partition_key=PartitionKey(path="/jobid")
)

# Setup Azure OpenAI

@app.post("/apply_to_job")
async def apply_to_job(
    name: str = Form(...),
    email: str = Form(...),
    job_id: str = Form(...),
    resume: UploadFile = None
):
    application_id = str(uuid.uuid4())

    # Read PDF content
    resume_bytes = await resume.read()
    resume_text = extract_text_from_pdf(resume_bytes)
    extracted_info = "abcdefgg"
    # extracted_info = await extract_info_with_openai(resume_text)
    item = {
        "id": application_id,
        "job_id": job_id,
        "name": name,
        "email": email,
        "resume_text": resume_text,
        "extracted_info": resume_text,
        "type":"applicant"
    }
    container.create_item(body=item)

    return JSONResponse(content={"application_id": application_id, "message": "Application submitted successfully!"})


class AzureResumeAnalysisAgent:
    def __init__(self, endpoint, api_key, deployment, api_version="2024-12-01-preview"):
        self.client = openai.ChatCompletion  # Assuming you're using OpenAI's Azure-based client
        self.deployment = deployment
        self.api_version = api_version
        self.api_base = endpoint
        self.api_key = api_key

    async def extract_info_with_openai(self, resume_text: str):
        # Format the resume content into a structured prompt for analysis
        prompt = f"""
        Extract key information from the following resume:
        - Full Name
        - Email
        - Phone Number
        - Skills
        - Experience Summary

        Resume:
        {resume_text}
        """

        # Making the API call to Azure OpenAI to extract relevant info from the resume
        try:
            response = self.client.create(
                model=self.deployment,  # Azure deployment name
                messages=[
                    {"role": "system", "content": "You are an expert resume parser."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=500,
                response_format="json",
            )

            # Extracting the response from the API call
            completion_tokens = response['usage']
            print("Completion Tokens:", completion_tokens)

            # Return the extracted information from the resume
            return response['choices'][0]['message']['content']
        # except openai.error.OpenAIError as e:
        #     raise Exception(f"OpenAI API error: {e}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")



class AnalyzeRequest(BaseModel):
    session_id: str




AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
AZURE_CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
connect_str = os.getenv("AZURE_CONNECTION_STRING")
container_name = os.getenv("AZURE_CONTAINER_NAME")
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_client = blob_service_client.get_container_client(container_name)

@app.post("/upload/")
async def upload_audio(session_id: str = Form(...), audio_file: UploadFile = File(...)):
    try:
        file_extension = audio_file.filename.split(".")[-1]
        unique_filename = f"{session_id}_{uuid.uuid4()}.{file_extension}"
        blob_client = container_client.get_blob_client('interview1.mp3')
        blob_client = container_client.get_blob_client(unique_filename)
        file_data = await audio_file.read()
        blob_client.upload_blob(file_data, overwrite=True)
        blob_url = blob_client.url
        analysis_result = f"Simulated transcript for file: {unique_filename}"

        return {
            "message": "Audio uploaded successfully to Azure!",
            "blob_url": blob_url,
            "analysis": analysis_result,
            "filename": unique_filename
        }

    except Exception as e:
        return {"error": str(e)}


class AzureVoiceAnalysisAgent:
    def __init__(self, endpoint, api_key, deployment, api_version="2024-12-01-preview"):
        self.client = AzureOpenAI(
            api_version=api_version,
            azure_endpoint=endpoint,
            api_key=api_key,
        )
        self.deployment = deployment

    def extract_audio_features(self, file_path: str):
        y, sr = librosa.load(file_path, sr=None)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch = np.mean(pitches[pitches > 0]) if np.any(pitches > 0) else 0
        energy = np.mean(librosa.feature.rms(y=y))

        return {
            "mfcc_std": float(np.std(mfcc)),
            "pitch_mean": float(pitch),
            "energy_mean": float(energy),
        }

    async def analyze_voice(self, file_path: str):
        features = self.extract_audio_features(file_path)

        prompt = f"""
You are an expert interview coach. Analyze the following audio features and assess the candidate's performance:

Features:
- MFCC Standard Deviation: {features['mfcc_std']}
- Average Pitch: {features['pitch_mean']}
- Average Energy: {features['energy_mean']}

Based on these:
Analyze the following extracted acoustic features from a candidate's interview audio:

MFCCs (20 coefficients over time)

Average pitch

Average energy (volume)

Based on these features, evaluate and report the candidate’s performance across the following traits:

Confidence:

High confidence is indicated by lower average pitch, louder energy, faster speaking rate, and falling intonation patterns.

Lower confidence may be indicated by high pitch variability, rising intonations, frequent pauses, or soft, hesitant speech.

Calmness:

Calm delivery is reflected in steady low pitch, moderate volume, and smooth, even pacing with minimal pitch jitter.

Nervousness or anxiety may be suggested by pitch breaks, choppy phrasing, or erratic loudness.

Energy/Engagement:

High energy is reflected in loud, lively, and quick speech with dynamic vocal variations.

Low energy is reflected in soft, slow, monotonous delivery and prolonged pauses.

Expressiveness (Timbre/MFCC Variance):

Higher MFCC standard deviation indicates more dynamic, engaging voice tone (positive if not excessive).

Very low MFCC variance may suggest flat affect or low engagement.

Actionable Insights:

For the recruiter:

Provide a summary score for each trait (Confidence, Calmness, Energy, Expressiveness) on a scale of 1–5.

Give a short paragraph on how these traits may impact the candidate’s fit for client-facing roles, leadership, teamwork, etc.

Highlight potential strengths (e.g., "Strong voice confidence, suitable for sales or leadership roles.") and developmental concerns (e.g., "Slight nervousness detected; may require coaching for high-pressure communication.").

For the candidate:

Offer positive feedback first (e.g., "Your calm, steady voice is a major strength.").

Suggest improvement areas (e.g., "Consider practicing speaking slightly louder and with more varied tone to convey greater enthusiasm.").

If applicable, suggest concrete exercises like voice modulation drills, breathing techniques, or pacing practice.

Important Constraints:

Base insights only on acoustic features, without speculating about personal attributes like ethnicity, gender, or native language.

Focus analysis on how the voice sounds, not what is said.

Maintain a professional, fair, and evidence-based tone in all outputs.

If voice features are ambiguous (e.g., mixed signals), explicitly mention that and suggest further evaluation through content analysis.
Respond only in JSON format.
"""

        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=[
                {"role": "system", "content": "You are an expert voice analysis AI."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=500,
            response_format={"type": "json_object"},
        )
        completion_tokens = response.usage
        print("Completion Tokens:", completion_tokens)
        return response.choices[0].message.content


import json
@app.post("/generate_report/")
async def generate_report(request: AnalyzeRequest):
    try:
        file_path = await download_audio_from_azure(request.session_id)
        agent = AzureVoiceAnalysisAgent(
            endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_KEY,
            deployment="gpt-4o"
        )
        report = await agent.analyze_voice(file_path)
        return {"report": report}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing audio: {str(e)}")


from fastapi import FastAPI, Form
from pydantic import BaseModel
from uuid import uuid4
from starlette.responses import JSONResponse


# Example schema for Job (you can expand this based on your DB model)
class Job(BaseModel):
    job_id: str
    description: str

# POST endpoint to create a job
@app.post("/create_job")
async def create_job(
    job_id: str = Form(...),
    description: str = Form(...)
):
    # Generate a unique job ID if not provided (or use the one from request)
    job_id = job_id or str(uuid4())

    # Create the job item to be posted into the DB
    job_item = {
        "id": job_id,
        "job_id": job_id,
        "description": description,
        "type": "job"
    }

    # Here you would typically save to the database
    container.create_item(body=job_item)  # Save to DB container

    return JSONResponse(content={"job_id": job_id, "message": "Job created successfully!"})

@app.get("/get_applications_by_job_id")
async def get_applications(job_id: str = Query(..., description="Get all job ids")):
    # Query the Cosmos DB for documents with type = "application" and the given job_id
    query = f"SELECT * FROM c WHERE c.type = 'applicant' AND c.job_id = '{job_id}'"

    items = []
    # Execute the query
    for item in container.query_items(query=query, enable_cross_partition_query=True):
        items.append(item)

    # Return the results
    if items:
        return JSONResponse(content={"applications": items})
    else:
        return JSONResponse(content={"message": "No applications found for the given job_id."})

@app.get("/get_all_jobs")
async def get_all_jobs():
    # Query the Cosmos DB for documents with type = "application" and the given job_id
    query = f"SELECT * FROM c WHERE c.type = 'job'"

    items = []
    # Execute the query
    for item in container.query_items(query=query, enable_cross_partition_query=True):
        items.append(item)

    # Return the results
    if items:
        return JSONResponse(content={"jobs": items})
    else:
        return JSONResponse(content={"message": "No jobs found."})


from fastapi.responses import JSONResponse

# === Define request body model ===
class AgentRequest(BaseModel):
    query: str


import openai
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class AgentRequest(BaseModel):
    query: str

class RecruiterAgent:
    def __init__(self, endpoint, api_key, deployment, api_version="2024-12-01-preview"):
        self.client = AzureOpenAI(
            api_version=api_version,
            azure_endpoint=endpoint,
            api_key=api_key,
        )
        self.deployment = deployment

    def generate_response(self, prompt: str):
        try:
            # Ensure the API call is made to Azure OpenAI
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=[
                    {"role": "system", "content": "You are a recruiter co-pilot. Help recruiters screen candidates, suggest hiring strategies, and optimize interviews. give data in one line"},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=500,
            )

            # The response is already in JSON format, so you can return it directly
            data = {
            "name": "John Doe",
            "age": 30,
            "city": "New York"
            }
            response_message = response.choices[0].message.content
            formatted_response = {
                'sender': 'agent',
                'text': response_message  # The actual response from the AI model
            }
            print(formatted_response)

            return formatted_response

            print(response.choices[0].message.content)
            
            response_message = "Hello! How can I assist you with recruitment today"
            return data

        except Exception as e:
            print(f"Error in recruiter_agent: {e}")
            return None

# Endpoint for recruiter agent interaction
@app.post("/api/agent")
async def recruiter_agent(request: AgentRequest):
    recruiter = RecruiterAgent(
            endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_KEY,
            deployment="gpt-4o"
        )  # Initialize the class instance
    agent_reply = recruiter.generate_response(request.query)  # Call the method for generating the response

    if agent_reply:
        return JSONResponse(content={"response": agent_reply})
    else:
        return JSONResponse(status_code=500, content={"error": "Failed to generate a response."})


live_adaptive_sessions = {}
# from azure.ai.generative import AsyncOpenAI
from typing import List, Dict

class AdaptiveInterviewAgent:
    def __init__(self, endpoint: str, api_key: str, deployment: str, job_description: str):
        self.client = AsyncAzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            azure_deployment=deployment,
            api_version="2024-02-15-preview"
        )
        self.job_description = job_description
        self.conversation: List[Dict[str, str]] = []  # stores full Q&A history

    async def generate_first_question(self):
        prompt = f"""You are an expert interviewer. Based on the following Job Description:

{self.job_description}

Generate the first interview question that assesses the candidate's basic fit and understanding. Be concise."""
        response = await self.client.chat.completions.create(
            model="gpt-4o",
            temperature=0.7,
            messages=[{"role": "user", "content": prompt}]
        )
        first_question = response.choices[0].message.content.strip()
        self.conversation.append({"role": "assistant", "content": first_question})
        return first_question

    async def generate_followup_question(self, candidate_answer: str):
        self.conversation.append({"role": "user", "content": candidate_answer})

        context_prompt = [
            {"role": "system", "content": f"You are a professional recruiter conducting an adaptive interview based on this job description:\n{self.job_description}"},
        ] + self.conversation + [
            {"role": "user", "content": "Based on the candidate's last answer, generate the next interview question. If appropriate, dive deeper or increase difficulty slightly. Ask one concise question."}
        ]

        response = await self.client.chat.completions.create(
            model="gpt-4o",
            temperature=0.7,
            messages=context_prompt
        )
        next_question = response.choices[0].message.content.strip()
        self.conversation.append({"role": "assistant", "content": next_question})
        return next_question

    async def summarize_interview(self):
        prompt = [
            {"role": "system", "content": "You are a recruiter summarizing an interview."},
            *self.conversation,
            {"role": "user", "content": "Summarize the candidate's overall performance, strengths, and areas of improvement in a professional tone."}
        ]

        response = await self.client.chat.completions.create(
            model="gpt-4o",
            temperature=0.5,
            messages=prompt
        )
        summary = response.choices[0].message.content.strip()
        return summary



class StartAdaptiveInterviewRequest(BaseModel):
    candidate_name: str
    job_description: str

# Endpoint to create a new session
@app.post("/create_session/")
async def create_session(questions: list, description: str):
    session_data = {
        "questions": questions,
        "description": description
    }
    session_id = store_session(session_data)  # Save session to Cosmos DB
    return {"message": "Session created successfully", "session_id": session_id}

# @app.post("/start_adaptive_interview")
# async def start_adaptive_interview(request: StartAdaptiveInterviewRequest):
#     session_id = str(uuid.uuid4())

#     agent = AdaptiveInterviewAgent(
#         endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
#         api_key=os.getenv("AZURE_OPENAI_KEY"),
#         deployment="gpt-4o",
#         job_description=request.job_description
#     )

#     first_question = await agent.generate_first_question()

#     live_adaptive_sessions[session_id] = {
#         "candidate_name": request.candidate_name,
#         "agent": agent
#     }
#     print(live_adaptive_sessions)

#     return {"session_id": session_id, "first_question": first_question}
import whisper

class StartAdaptiveInterviewRequest(BaseModel):
    candidate_name: str
    job_description: str
    identity_id: str


@app.post("/start_adaptive_interview")
async def start_adaptive_interview(request: StartAdaptiveInterviewRequest):
    session_id = "session"+str(uuid.uuid4())

    agent = AdaptiveInterviewAgent(
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        deployment="gpt-4o",
        job_description=request.job_description
    )

    first_question = await agent.generate_first_question()

    # Save session in Cosmos DB
    item = {
        "id": session_id,
        "questions": [first_question],
        "sessionid": session_id,
        "type": "session",
        "job_description": request.job_description,
        "idenitity_id": request.identity_id
    }
    container.create_item(body=item)

    return {"session_id": session_id, "first_question": first_question}

