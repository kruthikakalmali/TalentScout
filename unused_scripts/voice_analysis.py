# voice_analysis.py

import os
import librosa
import numpy as np
import uuid
import asyncio
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from openai import AzureOpenAI

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")

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

        return response.choices[0].message.content

# Azure Blob Storage setup
connect_str = os.getenv("AZURE_CONNECTION_STRING")
container_name = os.getenv("AZURE_CONTAINER_NAME")
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_client = blob_service_client.get_container_client(container_name)

async def download_audio_from_azure(filename: str) -> str:
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file_path = temp_file.name
            blob_client = container_client.get_blob_client(filename)
            blob_data = blob_client.download_blob()
            with open(file_path, "wb") as file:
                file.write(blob_data.readall())
            return file_path
    except Exception as e:
        raise Exception(f"Failed to download audio: {e}")
