

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
from AzureResumeAnalysisAgent import AzureResumeAnalysisAgent
from downloadaudiofromazure import download_audio_from_azure
from AnalyzeRequest import AnalyzeRequest
from AzureVoiceAnalysisAgent import AzureVoiceAnalysisAgent
from utils import convert_webm_to_mp3


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
