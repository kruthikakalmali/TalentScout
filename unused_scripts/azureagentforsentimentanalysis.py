# from openai import AzureOpenAI
# import librosa
# import numpy as np

# class AzureVoiceAnalysisAgent:
#     def __init__(self, endpoint, api_key, deployment, api_version="2024-12-01-preview"):
#         self.client = AzureOpenAI(
#             api_version=api_version,
#             azure_endpoint=endpoint,
#             api_key=api_key,
#         )
#         self.deployment = deployment

#     def extract_audio_features(self, file_path: str):
#         y, sr = librosa.load(file_path, sr=None)

#         mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
#         pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
#         pitch = np.mean(pitches[pitches > 0]) if np.any(pitches > 0) else 0
#         energy = np.mean(librosa.feature.rms(y=y))

#         return {
#             "mfcc_std": float(np.std(mfcc)),
#             "pitch_mean": float(pitch),
#             "energy_mean": float(energy),
#         }

#     async def analyze_voice(self, file_path: str):
#         features = self.extract_audio_features(file_path)

#         prompt = f"""
# You are an expert interview coach. Analyze the following audio features and assess the candidate's performance:

# Features:
# - MFCC Standard Deviation: {features['mfcc_std']}
# - Average Pitch: {features['pitch_mean']}
# - Average Energy: {features['energy_mean']}

# Based on these:
# - Estimate the candidate's **confidence level** (High/Moderate/Low)
# - Estimate **energy level** (High/Moderate/Low)
# - Estimate **calmness** (Very Calm/Slightly Nervous/Highly Nervous)
# - Give a **final score out of 3** (1 point for high confidence, 1 point for high energy, 1 point for very calmness)
# - Short Explanation (2-3 lines)
# - Analyse whether the person gave correct anaswers to the question and give "technical score" of 1 - 100 
# Respond only in JSON format.
# """

#         response = await self.client.chat.completions.create(
#             model=self.deployment,
#             messages=[
#                 {"role": "system", "content": "You are an expert voice analysis AI."},
#                 {"role": "user", "content": prompt},
#             ],
#             temperature=0.2,
#             max_tokens=500,
#             response_format="json",  # 💥 important for clean parsing
#         )

#         # Parse and return
#         return response.choices[0].message.content
