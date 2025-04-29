from typing import Optional
from fastapi import FastAPI, UploadFile, Form, File,HTTPException,Query
from fastapi.responses import StreamingResponse,JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import tempfile
from azure.storage.blob import BlobServiceClient
import uuid
from openai import AzureOpenAI,AsyncAzureOpenAI
import os
import librosa
import numpy as np
import subprocess
import ffmpeg
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from pydantic import BaseModel
import azure.cosmos
class AnalyzeRequest(BaseModel):
    session_id: str
from azure.cosmos import CosmosClient,PartitionKey
from pdfutility import extract_text_from_pdf
import random
import asyncio
from sklearn.metrics.pairwise import cosine_similarity
import requests
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, Form
import uuid
import openai
from fastapi import FastAPI, Form
from pydantic import BaseModel
from uuid import uuid4
from starlette.responses import JSONResponse
from pydantic import BaseModel
import json
from typing import List, Dict
from azure.communication.email import EmailClient
from ResumeScorer import ResumeScorer
from AzureResumeAnalysisAgent import AzureResumeAnalysisAgent
from downloadaudiofromazure import download_audio_from_azure
from AnalyzeRequest import AnalyzeRequest
from AzureVoiceAnalysisAgent import AzureVoiceAnalysisAgent
from AdaptiveInterviewAgent import AdaptiveInterviewAgent,StartAdaptiveInterviewRequest
from utils import convert_webm_to_mp3
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "https://talent-scout-teal.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
AZURE_CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
connect_str = os.getenv("AZURE_CONNECTION_STRING")
container_name = os.getenv("AZURE_CONTAINER_NAME")
# blob_service_client = BlobServiceClient.from_connection_string(connect_str)
# container_client = blob_service_client.get_container_client(container_name)


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

# @app.post("/apply_to_job")
# async def apply_to_job(
#     name: str = Form(...),
#     email: str = Form(...),
#     job_id: str = Form(...),
#     resume: UploadFile = None
# ):
#     application_id = "A"+str(random.randint(100000, 999999))

#     # Read PDF content
#     resume_bytes = await resume.read()
#     resume_text = extract_text_from_pdf(resume_bytes)
#     extracted_info = "abcdefgg"
#     # extracted_info = await extract_info_with_openai(resume_text)
#     item = {
#         "id": application_id,
#         "job_id": job_id,
#         "name": name,
#         "email": email,
#         "resume_text": resume_text,
#         "extracted_info": resume_text,
#         "type":"applicant",
#         "status": "APPLICATION_CREATED"
#     }
#     container.create_item(body=item)

#     return JSONResponse(content={"application_id": application_id, "message": "Application submitted successfully!"})

# class AnalyzeRequest(BaseModel):
#     session_id: str

AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
AZURE_CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
connect_str = os.getenv("AZURE_CONNECTION_STRING")
container_name = os.getenv("AZURE_CONTAINER_NAME")
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_client = blob_service_client.get_container_client(container_name)

@app.post("/upload")
async def upload_audio(session_id: str = Form(...), audio_file: UploadFile = File(...)):
    query = f"SELECT * FROM c WHERE c.id = '{session_id}'"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))

    if not items:
        raise HTTPException(status_code=404, detail="Session ID not found")

    item = items[0]
    identity_id = item.get("idenitity_id")  # or item["identity_id"] if it's a separate field

    query1 = f"SELECT * FROM c WHERE c.id = '{identity_id}'"
    items1 = list(container.query_items(query=query1, enable_cross_partition_query=True))
    if not items1:
        raise HTTPException(status_code=404, detail="Item not found")
    item1 = items1[0]
    item1["status"] = "INTERVIEW_COMPLETE"
    # try:
    container.replace_item(item=item1['id'], body=item1)

    try:
        file_data = await audio_file.read()

        # Convert WebM to MP3
        mp3_data = await convert_webm_to_mp3(file_data)

        # Create a unique filename
        unique_filename = f"{session_id}.mp3"
        blob_client = container_client.get_blob_client(unique_filename)

        # Upload mp3 data to Azure
        blob_client.upload_blob(mp3_data, overwrite=True)

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

import azure.cognitiveservices.speech as speechsdk
subscription_key = "72dmjGuP2icKJeQLcRqPvdLyhUXs3lVVYpuBrLmK2leXwDpg2lrAJQQJ99BDACYeBjFXJ3w3AAAYACOG81nO"
region = "eastus"


# from pydub import AudioSegment
# from imageio_ffmpeg import get_ffmpeg_exe
import torchaudio

all_results = []

# Define event callbacks
# def handle_final_result(evt):
#     print(f"Recognized: {evt.result.text}")
#     all_results.append(evt.result.text)

# def handle_canceled(evt):
#     print(f"Canceled: {evt.reason}")
#     if evt.reason == speechsdk.CancellationReason.Error:
#         print(f"Error details: {evt.error_details}")

# def handle_session_stopped(evt):
#     print("Session stopped.")
#     stop_event.set()

def recognized(evt):
    print(f"Recognized: {evt.result.text}")
    transcript.append(evt.result.text)

def canceled(evt):
    print(f"Canceled: {evt.reason}")
    if evt.reason == speechsdk.CancellationReason.Error:
        print(f"Error: {evt.error_details}")
    done.set()

def session_stopped(evt):
    print("Session stopped.")
    done.set()

import threading

@app.post("/generate_report")
async def generate_report(request: AnalyzeRequest):
    try:
        file_path = await download_audio_from_azure(request.session_id+".mp3")
        # CONVERT TO WAV FOR AZURE SPEECH SERVICES SDK
        waveform, sample_rate = torchaudio.load(file_path)
        resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
        waveform = resampler(waveform)
        if waveform.shape[0] > 1:
            waveform = waveform.mean(dim=0, keepdim=True)
        torchaudio.save("output.wav", waveform, 16000)
        # GENERATE TRANSCRIPT FOR AZURE SPEECH SERVICES SDK
        speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
        audio_config = speechsdk.audio.AudioConfig(filename="output.wav")
        recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        all_results = []
        def recognized(evt):
            if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                # print("Recognized:", evt.result.text)
                all_results.append(evt.result.text)
            elif evt.result.reason == speechsdk.ResultReason.NoMatch:
                print("No speech could be recognized")
        def session_stopped(evt):
            print("Session stopped.")
            stop_recognition()
        def canceled(evt):
            print("Canceled:", evt.reason)
            stop_recognition()
        def stop_recognition():
            recognizer.stop_continuous_recognition_async()
            done.set()
        from threading import Event
        done = Event()
        recognizer.recognized.connect(recognized)
        recognizer.session_stopped.connect(session_stopped)
        recognizer.canceled.connect(canceled)
        recognizer.start_continuous_recognition()
        done.wait()
        full_transcript = " ".join(all_results)
        print("\nFull Transcript:\n", full_transcript)

        agent = AzureVoiceAnalysisAgent(
            endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_KEY,
            deployment="gpt-4o"
        )
        query = f"SELECT * FROM c WHERE c.type = 'session' AND c.id = '{request.session_id}'"
        items = []
        print(request.session_id)
        for item in container.query_items(query=query, enable_cross_partition_query=True):
            items.append(item)
        questions = items[0]['questions']
        numbered_questions = '\n'.join(f"{i+1}. {q.strip()}" for i, q in enumerate(questions))
        print(numbered_questions)



        report = await agent.analyze_voice(file_path,full_transcript,numbered_questions)



        data = json.loads(report)
        return {"report": data}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing audio: {str(e)}")
# import shutil,logging
# try:
#     version = subprocess.check_output(["ffmpeg", "-version"]).decode().split("\n")[0]
#     logging.info(f"Found system ffmpeg: {version}")
# except Exception:
#     logging.error("ffmpeg binary not found on PATH")
# print("FFmpeg path:", shutil.which("ffmpeg"))




class Job(BaseModel):
    job_id: str
    description: str

# POST endpoint to create a job
@app.post("/create_job")
async def create_job(
    job_id: Optional[str] = Form(None),
    job_role: str = Form(...),
    description: str = Form(...),
    job_title: str = Form(...),
):
    # Generate a unique job ID if not provided (or use the one from request)
    job_id = job_id or str(uuid4())

    # Create the job item to be posted into the DB
    job_item = {
        "id": job_id,
        "job_id": job_id,
        "job_role": job_role,
        "description": description,
        "job_title":job_title,
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




# === Define request body model ===
class AgentRequest(BaseModel):
    query: str




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
                max_tokens=5000,
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



# Endpoint to create a new session
@app.post("/create_session/")
async def create_session(questions: list, description: str):
    session_data = {
        "questions": questions,
        "description": description
    }
    session_id = store_session(session_data)  # Save session to Cosmos DB
    return {"message": "Session created successfully", "session_id": session_id}


class StartAdaptiveInterviewRequest(BaseModel):
    job_id: str
    identity_id: str


@app.post("/start_adaptive_interview")
async def start_adaptive_interview(request: StartAdaptiveInterviewRequest):
    session_id = "session_"+str(uuid.uuid4())
    query = f"SELECT * FROM c WHERE c.id = '{request.identity_id}'"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    if not items:
        raise HTTPException(status_code=404, detail="Item not found")
    item = items[0]
    item["status"] = "INTERVIEW_IN_PROGRESS"
    # try:
    container.replace_item(item=item['id'], body=item)

    query = f"SELECT * FROM c WHERE c.type = 'job' AND c.job_id = '{request.job_id}'"

    items = []
    # Execute the query
    for item in container.query_items(query=query, enable_cross_partition_query=True):
        items.append(item)
    
    job_description_from_query = items[0]['description']

    agent = AdaptiveInterviewAgent(
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        deployment="gpt-4o",
        job_description=job_description_from_query
    )

    first_question = await agent.generate_first_question()

    # Save session in Cosmos DB
    item = {
        "id": session_id,
        "questions": [first_question],
        "sessionid": session_id,
        "type": "session",
        "job_description": job_description_from_query,
        "idenitity_id": request.identity_id
    }
    container.create_item(body=item)

    return {"session_id": session_id, "first_question": first_question}

class SubmitAdaptiveResponseRequest(BaseModel):
    session_id: str
    transcript: str


@app.post("/submit_adaptive_response")
async def submit_adaptive_response(request: SubmitAdaptiveResponseRequest):
    query = f"SELECT * FROM c WHERE c.id = '{request.session_id}'"
    try:
        items = []
        items = list(container.query_items(
    query=query,
    enable_cross_partition_query=True
))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Session not found")
    


    agent = AdaptiveInterviewAgent(
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        deployment="gpt-4o",
        job_description=items[0]["job_description"]
    )

    next_question = await agent.generate_followup_question(request.transcript)

    items[0]["questions"].append(next_question)
    container.replace_item(item=items[0], body=items[0])

    return {"next_question": next_question}

# from azure.communication.email import EmailContent, EmailAddress, EmailMessage


CONNECTION_STRING = "endpoint=https://talent-scout-communications.india.communication.azure.com/;accesskey=9qcnvbSEXGYg3cG5MnXca7zob0CIULNuyProAtkZcnFLgjhDf8drJQQJ99BDACULyCph2AV3AAAAAZCSZByy"

# Sender email (must be verified in ACS)
SENDER_EMAIL = "DoNotReply@0c9e4a27-5bc3-47b3-8206-cd4072e4d7cc.azurecomm.net"

OPENAI_API_KEY = AZURE_OPENAI_KEY
# Initialize Email Client
email_client = EmailClient.from_connection_string(CONNECTION_STRING)

# Initialize FastAPI
INTERVIEW_LINK = "https://talent-scout-teal.vercel.app/"

class SendEmailRequest(BaseModel):
    identity_id: str

@app.post("/send-email")
async def send_email(request: SendEmailRequest):
    query = f"SELECT * FROM c WHERE c.id = '{request.identity_id}'"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    if not items:
        raise HTTPException(status_code=404, detail="Item not found")
    item = items[0]
    item["status"] = "INTERVIEW_INVITE_SENT"
    # try:
    container.replace_item(item=item['id'], body=item)
    #     return {"message": "Status updated", "item": item}
    # except exceptions.CosmosHttpResponseError as e:
    #     raise HTTPException(status_code=500, detail=str(e))

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 10px;">
            <h2 style="color: #4CAF50;">Interview Invitation</h2>
            <p>Dear Candidate,</p>
            <p>We are excited to invite you for an interview with us!</p>
            <p>Please plan to take the interview within 48 hours of getting this invite</p>
            <p>Role:</b> Full Stack Developer (Backend Focus) </p>
            <p>JobID:</b> J908765</p>
            <p>Please click the button below to join the interview:</p>
            <p style="text-align: center;">
                <a href="{INTERVIEW_LINK}" style="background-color: #4CAF50; color: white; padding: 14px 25px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; font-size: 16px;">
                    Join Interview
                </a>
            </p>
            <p>Best regards,<br>TalentScout Team</p>
        </div>
    </body>
    </html>
    """

    message = {
        "senderAddress": SENDER_EMAIL,
        "recipients": {
            "to": [{"address": items[0]['email']}]
        },
        "content": {
            "subject": "You're Invited: Interview with TalentScout",
            "html": html_content,
            "plainText": "Dear Candidate, You are invited for an interview. Please check your email in a browser that supports HTML to see the invitation."
        }
    }

    poller = email_client.begin_send(message)
    result = poller.result()

    return {"message": "Email sent successfully", "status": result}







api_key = "81ClR2uk3VJCLU3i78xpXmLDRPjV4BtlUXOMjP4kgHy4j36leVzsJQQJ99BDACYeBjFXJ3w3AAABACOGB5ka"
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")
url = f"https://vector1.openai.azure.com/openai/deployments/text-embedding-ada-002/embeddings?api-version=2023-05-15"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Function to get embedding via REST API
def get_embedding(text):
    data = {
        "input": [text]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['data'][0]['embedding']
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")






@app.get("/get_top_applications_by_job_id")
async def get_top_applications(job_id: str = Query(..., description="Get all job ids")):
    # Step 1: Get JD text (Job Description)
    query = f"SELECT * FROM c WHERE c.type = 'applicant' AND c.job_id = '{job_id}'"
    applicants = []
    for item in container.query_items(query=query, enable_cross_partition_query=True):
        applicants.append(item)
    
    jd_query = f"SELECT * FROM c WHERE c.type = 'job' AND c.id = '{job_id}'"
    jobs = []
    for item in container.query_items(query=jd_query, enable_cross_partition_query=True):
        jobs.append(item)
    
    jd_text = jobs[0]['description']
    print(f"Job Description: {jd_text}")

    # Step 2: Get the job description embedding
    jd_embedding = get_embedding(jd_text)

    # Step 3: Process each applicant's resume
    applicant_embeddings = []
    applicant_texts = []
    for app in applicants:
        text = app.get("extracted_info", "")
        applicant_texts.append(text)
        emb = get_embedding(text)  # Make sure to await async get_embedding
        applicant_embeddings.append(emb)

    # Step 4: Calculate cosine similarity
    scores = []
    for idx, resume_emb in enumerate(applicant_embeddings):
        # Convert both jd_embedding and resume_emb to numpy arrays
        jd_embedding_np = np.array(jd_embedding)
        resume_emb_np = np.array(resume_emb)

        similarity = cosine_similarity(jd_embedding_np.reshape(1, -1), resume_emb_np.reshape(1, -1))[0][0]
        scores.append((similarity, idx))

    # Step 5: Sort the applicants by similarity score (descending order)
    scores.sort(reverse=True)

    # Step 6: Select the top N applicants (top 20 in this case)
    top_N = 10
    top_candidates = [applicants[idx] for _, idx in scores[:top_N]]

    final_results = []
    for similarity, applicant in zip([score[0] for score in scores[:top_N]], top_candidates):
        resume_text = applicant.get("resume_text", "")

        # llm_eval = await score_resume_with_llm(jd_text, resume_text)
        agent = ResumeScorer(
            endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_KEY,
            deployment="gpt-4o"
        )
        report = await agent.score_resume(jd_text,resume_text)
        
        if report:
            final_results.append({
            "applicant_id": applicant.get("id"),
            "name": applicant.get("name"),
            "email": applicant.get("email"),
            "similarity_score": round(similarity, 4),
            "skill_match": report.get("skill_match"),
            "experience_relevance": report.get("experience_relevance"),
            "cultural_fit_guess": report.get("cultural_fit_guess"),
            "strengths": report.get("strengths"),
            "potential_gaps": report.get("potential_gaps"),
            "overall_fit_summary": report.get("overall_fit_summary"),
        })
    
    print(final_results)      
    await asyncio.sleep(2)
    # if(final_results!=[]):
    return JSONResponse(content={"top_applications": final_results})





# -------------- New: Azure Search Import -----------------
# (no special import needed because we will call REST API manually)

# -------- Azure Cognitive Search configuration ------------
AZURE_SEARCH_ENDPOINT = "https://vectorsearchtalentscout.search.windows.net"  # like https://<search-service>.search.windows.net
AZURE_SEARCH_API_KEY = "7ec74giuolqkWiIOeHl6luXvqh05T7VizeRKYcRyWSAzSeC1J3yz"
AZURE_SEARCH_INDEX_NAME = "resumes"  # Name of your Azure Search index

search_headers = {
    "Content-Type": "application/json",
    "api-key": AZURE_SEARCH_API_KEY
}

# ------------- Reuse your Azure OpenAI endpoint ------------
api_key = "G0EcfY6zYcCx9QvKTGe1UruDMIEGph1MLUIVquMbipzdQDdfvDf1JQQJ99BDACHYHv6XJ3w3AAAAACOG0mTU"
url = f"https://ai-kunalmodi0374ai269865417376.openai.azure.com/openai/deployments/text-embedding-ada-002/embeddings?api-version=2023-05-15"
embedding_headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def get_embedding(text):
    data = {"input": [text]}
    response = requests.post(url, headers=embedding_headers, json=data)
    if response.status_code == 200:
        return response.json()['data'][0]['embedding']
    else:
        raise Exception(f"Error in embedding generation: {response.text}")

# -------------------------------------------------------------
# ------------- Upload applicant to Azure Search -------------
async def upload_applicant_to_search(applicant):
    embedding = get_embedding(applicant['resume_text'])
    
    upload_url = f"{AZURE_SEARCH_ENDPOINT}/indexes/{AZURE_SEARCH_INDEX_NAME}/docs/index?api-version=2023-11-01"
    payload = {
        "value": [
            {
                "@search.action": "upload",
                "id": applicant['id'],
                "name": applicant['name'],
                "email": applicant['email'],
                "resume_text": applicant['resume_text'],
                "resume_embedding": embedding
            }
        ]
    }
    response = requests.post(upload_url, headers=search_headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Failed to upload to Azure Search: {response.text}")

# --------------------------------------------------------------
# -------------- Now: Updated /get_top_applications -----------
@app.get("/get_top_applications_by_job_id2")
async def get_top_applications2(job_id: str = Query(..., description="Get all job ids")):
    # Step 1: Get Job Description
    jd_query = f"SELECT * FROM c WHERE c.type = 'job' AND c.id = '{job_id}'"
    jobs = []
    for item in container.query_items(query=jd_query, enable_cross_partition_query=True):
        jobs.append(item)
    if not jobs:
        return JSONResponse(content={"error": "Job not found"}, status_code=404)

    jd_text = jobs[0]['description']
    jd_embedding = get_embedding(jd_text)

    # Step 2: Search Azure Cognitive Search for top matching resumes
    search_url = f"{AZURE_SEARCH_ENDPOINT}/indexes/{AZURE_SEARCH_INDEX_NAME}/docs/search?api-version=2023-11-01"

    search_body = {
        "vector": {
            "value": jd_embedding,
            "fields": "resume_embedding",
            "k": 10  # Get top 10 applicants
        },
        "select": "id,name,email,resume_text"
    }

    response = requests.post(search_url, headers=search_headers, json=search_body)
    if response.status_code != 200:
        raise Exception(f"Azure Search failed: {response.text}")

    search_results = response.json()['value']

    # Step 3: For each matched resume, score it via ResumeScorer LLM
    final_results = []

    for result in search_results:
        applicant_id = result['id']
        name = result.get('name', '')
        email = result.get('email', '')
        resume_text = result.get('resume_text', '')

        # LLM based scoring (you already have)
        agent = ResumeScorer(
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            deployment="gpt-4o"
        )
        report = await agent.score_resume(jd_text, resume_text)

        if report:
            final_results.append({
                "applicant_id": applicant_id,
                "name": name,
                "email": email,
                "skill_match": report.get("skill_match"),
                "experience_relevance": report.get("experience_relevance"),
                "cultural_fit_guess": report.get("cultural_fit_guess"),
                "strengths": report.get("strengths"),
                "potential_gaps": report.get("potential_gaps"),
                "overall_fit_summary": report.get("overall_fit_summary"),
            })

    return JSONResponse(content={"top_applications": final_results})



@app.post("/apply_to_job")
async def apply_to_job(
    name: str = Form(...),
    email: str = Form(...),
    job_id: str = Form(...),
    resume: UploadFile = None
):
    application_id = "A"+str(random.randint(100000, 999999))

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
        "type":"applicant",
        "status": "APPLICATION_CREATED"
    }
    await upload_applicant_to_search(item)
    container.create_item(body=item)

    return JSONResponse(content={"application_id": application_id, "message": "Application submitted successfully!"})



@app.get("/get_all_interview_completed_applicants_by_job_id")
async def get_all_interview_completed_applicants_by_jobid(job_id: str = Query(..., description="get_all_interview_completed_applicants_by_jobid")):
     # Query the Cosmos DB for documents with type = "application" and the given job_id
     query = f"SELECT * FROM c WHERE c.type = 'applicant' AND c.job_id = '{job_id}' and c.status='INTERVIEW_COMPLETE'"
 
     items = []
     # Execute the query
     for item in container.query_items(query=query, enable_cross_partition_query=True):
         items.append(item)
 
     # Return the results
     if items:
         return JSONResponse(content={"applications": items})
     else:
         return JSONResponse(content={"message": "No applications found for the given job_id."})
 

@app.get("/get_all_interview_completed_applicants")
async def get_all_interview_completed_applicants():
     # Query the Cosmos DB for documents with type = "application" and the given job_id
     query = f"SELECT * FROM c WHERE c.type = 'applicant' and c.status='INTERVIEW_COMPLETE'"
 
     items = []
     # Execute the query
     for item in container.query_items(query=query, enable_cross_partition_query=True):
        query1 = f"SELECT * FROM c WHERE c.type = 'session' and c.idenitity_id='{item['id']}'"
        items1 = []
        for item1 in container.query_items(query=query1, enable_cross_partition_query=True):
            items1.append(item1)
        
        session_id = items1[0]['id']
        item['session_id'] = session_id
        items.append(item)
 
     # Return the results
     if items:
         return JSONResponse(content={"applications": items})
     else:
         return JSONResponse(content={"message": "No applications with completed interview"})
 

from msal import PublicClientApplication

CLIENT_ID = "c52cb629-9959-4b1a-a960-8ac7c9a4ef3a"
TENANT_ID = "c7c3caf6-bcf8-45fe-a2f4-c976313d4a93"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["Mail.Send"]
client_id = CLIENT_ID
client_secret = "k128Q~kCFM-xAIJVTAls8MzDrpez2_jumzMRvbDI"
tenant_id = TENANT_ID
 
import os
from msal import PublicClientApplication
# from config import CLIENT_ID, AUTHORITY, SCOPES
from msal import ConfidentialClientApplication

def get_access_token():
    # client_id = "your_client_id"
    # client_secret = "your_client_secret"  # 🔥 Add this
    # tenant_id = "your_tenant_id"

    authority = f"https://login.microsoftonline.com/{tenant_id}"
    scopes = ["https://graph.microsoft.com/.default"]

    app = ConfidentialClientApplication(
        client_id,
        authority=authority,
        client_credential=client_secret,
    )

    result = app.acquire_token_for_client(scopes=scopes)

    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception("Could not acquire token: " + str(result))

import requests
user_id="951b9783-2b72-4aad-839c-8a9da796bda4"
def send_email():
    token = get_access_token()
    print("GOT ACCESS TOKEN")
    url = "https://graph.microsoft.com/v1.0/users/951b9783-2b72-4aad-839c-8a9da796bda4/sendMail"
    print(url)  # Replace {user_id} with a valid user ID
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    
    # Construct your email message content
    email_msg = {
        "message": {
            "subject": "Interview Summary: Candidate Alice",
            "body": {
                "contentType": "HTML",
                "content": "<h2>Interview Summary</h2><p>Candidate Alice: Strong technical skills, but needs to improve system design fundamentals.</p>"
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": "recruiter@example.com"
                    }
                }
            ]
        },
        "saveToSentItems": "true"
    }
    
    response = requests.post(url, headers=headers, json=email_msg)

    if response.status_code == 202:
        print("Email sent successfully!")
    else:
        print("Error sending email:", response.status_code, response.text)




# send_email()


def get_user_id_by_email(token, email):
    url = f"https://graph.microsoft.com/v1.0/users/{email}"  # Use the email address here
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        return user_data['id']  # This will be the unique `user_id` of the specified email
    else:
        raise Exception("Error getting user ID:", response.status_code, response.text)
token = get_access_token()
# print(token)  # Get your access token as before

def get_user_id_by_email(token, email):
    url = f"https://graph.microsoft.com/v1.0/users/{email}"  # Use the email address here
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        return user_data['id']  # This will be the unique `user_id` of the specified email
    else:
        raise Exception("Error getting user ID:", response.status_code, response.text)




user_id = get_user_id_by_email(token,"KruthikaKalmali@LowesIndia366.onmicrosoft.com")
print("user id is" + user_id)
# print("User ID:", user_id)

# send_email()



import openai
import requests
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Azure OpenAI Configuration
api_key = "G0EcfY6zYcCx9QvKTGe1UruDMIEGph1MLUIVquMbipzdQDdfvDf1JQQJ99BDACHYHv6XJ3w3AAAAACOG0mTU"
openai_endpoint = "https://ai-kunalmodi0374ai269865417376.openai.azure.com/"
deployment_id = "text-embedding-ada-002"  # Replace with your deployment ID

# Azure Search Configuration
AZURE_SEARCH_ENDPOINT = "https://vectorsearchtalentscout.search.windows.net"
AZURE_SEARCH_API_KEY = "7ec74giuolqkWiIOeHl6luXvqh05T7VizeRKYcRyWSAzSeC1J3yz"
AZURE_SEARCH_INDEX_NAME = "resumes"

# Configure OpenAI API client
openai.api_key = api_key
openai.api_base = openai_endpoint

# Azure Cognitive Services API setup (for embedding generation)
AZURE_COGNITIVE_SERVICES_API_KEY = AZURE_SEARCH_API_KEY
AZURE_COGNITIVE_SERVICES_ENDPOINT = AZURE_SEARCH_ENDPOINT

# Azure Search API setup
# AZURE_SEARCH_ENDPOINT = "https://YOUR_SEARCH_ENDPOINT.search.windows.net"
# AZURE_SEARCH_API_KEY = "YOUR_AZURE_SEARCH_API_KEY"
# AZURE_SEARCH_INDEX_NAME = "resumes"  # The name of the Azure Search index where the resumes are stored

# Function to generate embeddings using Azure Cognitive Services Text Analytics API
# def generate_embedding_for_input(input_text):
#     url = f"{AZURE_COGNITIVE_SERVICES_ENDPOINT}/text/analytics/v3.0-preview.1/entities/recognition/general"

    
#     headers = {
#         "Ocp-Apim-Subscription-Key": AZURE_COGNITIVE_SERVICES_API_KEY,
#         "Content-Type": "application/json"
#     }
    
#     data = {
#         "documents": [
#             {
#                 "id": "1",
#                 "language": "en",
#                 "text": input_text
#             }
#         ]
#     }
    
#     response = requests.post(url, headers=headers, json=data)
#     print(response)

def generate_embedding_for_input(input_text):
    response = openai.Embedding.create(
        input=input_text,
        deployment_id=deployment_id,     # Your Azure OpenAI deployment name
        api_version="2023-05-15"         # Use your correct API version
    )
    embedding = response["data"][0]["embedding"]
    # print(response)
    return embedding


# # Function to search the Azure Cognitive Search index for top 3 matching resumes
def search_resumes(embedding):
    search_url = f"{AZURE_SEARCH_ENDPOINT}/indexes/{AZURE_SEARCH_INDEX_NAME}/docs/search?api-version=2023-07-01-Preview"

    
    headers = {
        'Content-Type': 'application/json',
        'api-key': AZURE_SEARCH_API_KEY
    }
    print(len(embedding))
    print(type(embedding[0]))
    search_body = {
    "vector": {
        "value": embedding,
        "fields": "resume_embedding",
         "k": 3
    }
}
    
    response = requests.post(search_url, headers=headers, json=search_body)
    # print(response.text)
    return response
import json
# Main chatbot function
def chatbot(user_input):
    embedding = get_embedding(user_input)
    search_results = search_resumes(embedding)
    decoded_response = search_results.content.decode("utf-8")
    parsed_response = json.loads(decoded_response)
    print(parsed_response['value'])
    items=[]
    for result in parsed_response['value']:
        score = result["@search.score"]
        id = result["id"]
        name = result["name"]
        email = result["email"]
        item = {"name":name,"email":email}
        items.append(item)
        # items.add(id)
        # items.add(name)
        # items.add(email)
        print(f"ID: {id}")
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Score: {score}")
        print("-" * 40)
    return items
# chatbot("backend")

class ChatRequest(BaseModel):
    message: str
    mode: str  # 'vector' or 'openai'


@app.post("/chat")
def chat_route(request: ChatRequest):
    # data = request.json()
    mode = request.mode
    message = request.message

    if mode == "vector":
        results = chatbot(message)
        return {"reply": json.dumps(results)}
    elif mode == "openai":
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message}]
        )
        return {"reply": response.choices[0].message['content']}

@app.post("/chat")
async def chat(req: ChatRequest):
    if req.mode == "vector":
        embedding = get_embedding(req.message)
        results = chatbot(message)
        return results
        # if not results.get("value"):
        #     return {"reply": "No matching resumes found."}

        # reply = "Here are the top matches:\n\n"
        # for r in results["value"]:
        #     reply += f"👤 Name: {r['name']}\n📧 Email: {r['email']}\n📊 Match Score: {round(r['@search.score'] * 100, 2)}%\n\n"
        # return {"reply": reply.strip()}

    elif req.mode == "openai":
        # prompt = f"You are a helpful recruiter assistant. User asked: '{req.message}'"
        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=[{"role": "user", "content": prompt}]
        # )
        # return {"reply": response['choices'][0]['message']['content']}
        return null

    else:
        return {"reply": "Invalid mode."}
