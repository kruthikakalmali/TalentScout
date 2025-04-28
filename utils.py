

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


async def convert_webm_to_mp3(file_data: bytes) -> bytes:
    """Converts WebM audio bytes to MP3 bytes using FFmpeg."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as temp_input:
        temp_input.write(file_data)
        temp_input.flush()
        input_path = temp_input.name

    output_path = input_path.replace(".webm", ".mp3")

    try:
        # FFmpeg command to convert
        subprocess.run(
            ["ffmpeg", "-i", input_path, "-f", "mp3", "-y", output_path],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        with open(output_path, "rb") as f:
            mp3_data = f.read()

        return mp3_data

    finally:
        # Always clean up temp files
        os.unlink(input_path)
        if os.path.exists(output_path):
            os.unlink(output_path)