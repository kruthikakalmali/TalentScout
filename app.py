# # app.py

# from fastapi import FastAPI, UploadFile, File, Form
# import uuid
# import os
# import aiofiles

# app = FastAPI()

# UPLOAD_DIR = "uploaded_audio"
# os.makedirs(UPLOAD_DIR, exist_ok=True)

# @app.post("/upload_audio/")
# async def upload_audio(session_id: str = Form(...), current_question: str = Form(...), file: UploadFile = File(...)):
#     # Create a unique filename
#     filename = f"{session_id}_{uuid.uuid4()}.wav"
#     file_path = os.path.join(UPLOAD_DIR, filename)

#     # Save the uploaded audio file
#     async with aiofiles.open(file_path, 'wb') as out_file:
#         content = await file.read()
#         await out_file.write(content)

#     print(f"Received and saved file at: {file_path}")
#     print(f"Session ID: {session_id}")
#     print(f"Current Question: {current_question}")

#     # SIMULATED ANALYSIS
#     simulated_text = f"Simulated transcript for file: {filename}"

#     # Here you could call Azure Whisper/OpenAI API etc.

#     return {
#         "message": "Audio received successfully.",
#         "file_path": file_path,
#         "analysis": simulated_text
#     }


from fastapi import FastAPI, UploadFile, File
from azure.storage.blob import BlobServiceClient
import uuid
import os

app = FastAPI()

# Azure Storage Connection Settings
AZURE_CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
AZURE_CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME")

blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)

@app.post("/upload/")
async def upload_audio(session_id: str, audio_file: UploadFile = File(...)):
    try:
        # Generate unique filename
        file_extension = audio_file.filename.split(".")[-1]
        unique_filename = f"{session_id}_{uuid.uuid4()}.{file_extension}"

        # Upload file to Azure Blob Storage
        blob_client = container_client.get_blob_client('interview1.mp3')
        blob_client = container_client.get_blob_client(unique_filename)
        file_data = await audio_file.read()
        blob_client.upload_blob(file_data, overwrite=True)

        # Generate Blob URL
        blob_url = blob_client.url

        # Simulate Analysis
        analysis_result = f"Simulated transcript for file: {unique_filename}"

        return {
            "message": "Audio uploaded successfully to Azure!",
            "blob_url": blob_url,
            "analysis": analysis_result
        }

    except Exception as e:
        return {"error": str(e)}

# asdf
#fvgbhnjmk,