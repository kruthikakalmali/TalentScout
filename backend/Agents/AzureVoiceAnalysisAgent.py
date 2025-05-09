

from typing import Optional
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
from fastapi.responses import JSONResponse
import uuid
import openai
import os
from fastapi import FastAPI, Form
from pydantic import BaseModel
from uuid import uuid4
from starlette.responses import JSONResponse
import openai
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json
from fastapi.responses import JSONResponse
from typing import List, Dict
import whisper
from azure.communication.email import EmailClient
from ResumeScorer import ResumeScorer
from backend.Agents.AzureResumeAnalysisAgent import AzureResumeAnalysisAgent
from downloadaudiofromazure import download_audio_from_azure
from AnalyzeRequest import AnalyzeRequest

json1 = { "audio_analysis": { "confidence_score": 0, "calmness_score": 0, "energy_score": 0, "expressiveness_score": 0, "recruiter_summary": "...", "candidate_feedback": { "positive": "...", "suggestions": "..." } }, "technical_analysis": { "per_question": [ { "question": "...", "answer_excerpt": "...", "scores": { "correctness": 0, "completeness": 0, "relevance": 0, "clarity": 0, "depth": 0 }, "summary": "..." } ], "overall_technical_score": 0, "recruiter_summary": "...", "candidate_feedback": { "positive": "...", "suggestions": "..." } } }
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

    async def analyze_voice(self, file_path: str,transcript: str,questions: str):
        features = self.extract_audio_features(file_path)

        prompt = f"""
You are an expert interview coach with specialties in both **acoustic behavioral analysis** and **technical content evaluation**. 

You are provided with:
- Audio features from a candidate's interview response:
  - MFCC Standard Deviation: {features['mfcc_std']}
  - Average Pitch: {features['pitch_mean']}
  - Average Energy: {features['energy_mean']}
- Transcript of the candidate's responses: {transcript}
- List of interview questions: {questions}

Your task is to perform a two-part analysis:

### Part 1: Audio-Based Voice Analysis
Analyze the extracted acoustic features from the candidate’s audio recording:

- MFCCs (20 coefficients over time)
- Average pitch
- Average energy (volume)

Evaluate the candidate’s performance across these **behavioral voice traits**:

**Confidence**  
- High: lower pitch, louder energy, faster speaking rate, falling intonation.  
- Low: high pitch variability, rising intonation, soft/hesitant speech.

**Calmness**  
- High: steady low pitch, smooth pacing, even energy.  
- Low: pitch breaks, choppy phrasing, erratic volume.

**Energy / Engagement**  
- High: loud, lively, quick speech with vocal variation.  
- Low: soft, slow, monotonous delivery.

**Expressiveness (Timbre / MFCC Std Dev)**  
- High MFCC std indicates vocal dynamism and engagement.  
- Very low MFCC std suggests flat affect or low engagement.

For the **recruiter**, give a score from 1–5 for each trait and a brief summary on:
- Fit for roles requiring communication (sales, leadership, collaboration)
- Strengths and developmental concerns

For the **candidate**, provide:
- Positive voice-based feedback
- Improvement suggestions (if any), with actionable techniques like breathing, pacing, or modulation drills

### Part 2: Technical Content Analysis
Using the provided list of questions and the transcripted answers, evaluate the **technical quality** of the responses. Focus on:

- **Correctness** – Did the candidate give accurate and factually correct answers?
- **Completeness** – Were key points covered, or were responses vague or partial?
- **Relevance** – Were the answers well-aligned with the question's intent?
- **Clarity** – Was the explanation logically structured and easy to follow?
- **Depth** – Did the answer demonstrate insight, practical understanding, and examples?

Provide a 1–5 score for each of the above criteria per question. Also give:

- **Per-question analysis summary**  
- A total **Technical Competency Score (1–5)** across all responses

Finally, provide:

- For the **recruiter**: A brief overview of the candidate’s technical aptitude and communication clarity in answering job-relevant questions.
- For the **candidate**: Constructive feedback highlighting strengths and areas for content improvement. Suggest study/practice areas if gaps were found.

### Output Format
Respond only in **JSON** format with the same structure as {json1}


### Important Constraints:
- Do **not** speculate on ethnicity, gender, or native language.
- Focus only on **how** the candidate spoke and **what** they said technically.
- If acoustic traits or technical content is ambiguous, mention it and recommend further review.

"""

        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=[
                {"role": "system", "content": "You are an expert voice analysis AI."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=5000,
            response_format={"type": "json_object"},
        )
        completion_tokens = response.usage
        print("Completion Tokens:", completion_tokens)
        return response.choices[0].message.content

