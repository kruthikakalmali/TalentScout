

from fastapi import FastAPI, UploadFile, File,HTTPException
from fastapi.responses import StreamingResponse
import tempfile
from azure.storage.blob import BlobServiceClient
import uuid
from openai import AzureOpenAI
import os
import librosa
import numpy as np
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import tempfile
from pydantic import BaseModel
import azure.cosmos
class AnalyzeRequest(BaseModel):
    session_id: str
from azure.cosmos import CosmosClient,PartitionKey
from pdfutility import extract_text_from_pdf
from downloadaudiofromazure import download_audio_from_azure
app = FastAPI()

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

@app.post("/apply")
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
        "extracted_info": resume_text
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
async def upload_audio(session_id: str, audio_file: UploadFile = File(...)):
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
            "analysis": analysis_result
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