

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

class QueryAgent:
    def __init__(self, endpoint, api_key, deployment, api_version="2024-12-01-preview"):
        self.client = AsyncAzureOpenAI(
            api_version=api_version,
            azure_endpoint=endpoint,
            api_key=api_key,
        )
        self.deployment = deployment
        self.chat_memory = {}  # session_id -> list of messages

    def _get_context(self, session_id):
        return self.chat_memory.get(session_id, [])

    def _save_context(self, session_id, messages):
        self.chat_memory[session_id] = messages[-10:]  # keep last 10 messages

    async def chat(self, session_id: str, user_message: str) -> str:
        context = self._get_context(session_id)
        context.append({"role": "user", "content": user_message})

        response = await self.client.chat.completions.create(
            model=self.deployment,
            messages=context,
            temperature=0.3,
        )

        reply = response.choices[0].message.content
        context.append({"role": "assistant", "content": reply})
        self._save_context(session_id, context)

        return reply
    def clear_context(self, sessionid: str):
        if sessionid in self.chat_memory:
            del self.chat_memory[sessionid]

