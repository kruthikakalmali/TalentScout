import os
import librosa
import numpy as np
import uuid
import asyncio
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from fastapi.responses import StreamingResponse
import tempfile
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

        # Extract MFCC features
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
        # Extract pitch and magnitude
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch = np.mean(pitches[pitches > 0]) if np.any(pitches > 0) else 0
        # Extract energy (RMS)
        energy = np.mean(librosa.feature.rms(y=y))

        return {
            "mfcc_std": float(np.std(mfcc)),
            "pitch_mean": float(pitch),
            "energy_mean": float(energy),
        }

    async def analyze_voice(self, file_path: str):
        # Extract features from the audio file
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

        # Parse and return response
        return response.choices[0].message.content


# Azure Blob Storage setup
connect_str =  os.getenv("AZURE_CONNECTION_STRING")
container_name =  os.getenv("AZURE_CONTAINER_NAME")
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


async def main():
    file_name = "interview1.mp3"
    # Step 1: Download file from Azure Blob Storage to a temporary file
    file_path = await download_audio_from_azure("session-456_692a156b-6e9e-46f5-aab5-2c841cd76e61.mp3")
    
    # Step 2: Create the agent and analyze the audio file
    agent = AzureVoiceAnalysisAgent(
        endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_KEY,
        deployment="gpt-4o"
    )
    report = await agent.analyze_voice(file_path)
    
    print(report)


# Run the main function
asyncio.run(main())
