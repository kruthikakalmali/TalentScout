


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
connect_str = os.getenv("AZURE_CONNECTION_STRING")
container_name = os.getenv("AZURE_CONTAINER_NAME")
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_client = blob_service_client.get_container_client(container_name)

async def download_audio_from_azure(filename: str) -> str:
    """Download the MP3 file from Azure Blob Storage and save to a temporary directory"""
    try:
        # Create a temporary file to save the audio
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file_path = temp_file.name  # Get the temporary file path
            blob_client = container_client.get_blob_client(filename)
            blob_data = blob_client.download_blob()
            with open(file_path, "wb") as file:
                file.write(blob_data.readall())
            return file_path
    except Exception as e:
        raise Exception(f"Failed to download audio: {e}")
