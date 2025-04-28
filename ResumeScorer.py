

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
import json
from sklearn.metrics.pairwise import cosine_similarity
import requests
from fastapi.middleware.cors import CORSMiddleware



class ResumeScorer:
    def __init__(self, endpoint, api_key, deployment, api_version="2024-12-01-preview"):
        self.client = AsyncAzureOpenAI(
            api_version=api_version,
            azure_endpoint=endpoint,
            api_key=api_key,
        )
        self.deployment = deployment

    async def score_resume(self, jd_text: str,resume_text: str):
        prompt = f"""
You are a professional recruiter.

Given the following Job Description and Resume, score the resume:

Job Description:
{jd_text}

Candidate Resume:
{resume_text}

Evaluate and return JSON with:
- skill_match (0-10)
- experience_relevance (0-10)
- cultural_fit_guess (0-10)
- strengths (text)
- potential_gaps (text)
- overall_fit_summary (text)
"""

        response = await self.client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        print(content)
        try:
            report = json.loads(content)
            return report
        except Exception as e:
            print("Error parsing LLM response:", e)
            return None
