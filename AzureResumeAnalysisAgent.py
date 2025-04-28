from ResumeScorer import ResumeScorer



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
