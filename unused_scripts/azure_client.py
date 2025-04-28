# import azure.cognitiveservices.speech as speechsdk
# from app.config import AZURE_SPEECH_KEY, AZURE_SPEECH_REGION

# def create_speech_recognizer():
#     speech_config = speechsdk.SpeechConfig(
#         subscription=AZURE_SPEECH_KEY,
#         region=AZURE_SPEECH_REGION
#     )
#     audio_config = speechsdk.AudioConfig(use_default_microphone=False)
#     recognizer = speechsdk.SpeechRecognizer(speech_config, audio_config)
#     return recognizer


# import requests
# from app.config import AZURE_TEXT_ANALYTICS_KEY, AZURE_TEXT_ANALYTICS_ENDPOINT

# def analyze_text(text: str):
#     url = f"{AZURE_TEXT_ANALYTICS_ENDPOINT}/text/analytics/v3.2/sentiment"
#     headers = {
#         "Ocp-Apim-Subscription-Key": AZURE_TEXT_ANALYTICS_KEY,
#         "Content-Type": "application/json"
#     }
#     data = {"documents": [{"id": "1", "language": "en", "text": text}]}
#     response = requests.post(url, headers=headers, json=data)
#     return response.json()

# def evaluate_answer(prompt: str):
#     url = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/gpt-4/chat/completions?api-version=2023-05-15"
#     headers = {
#         "api-key": AZURE_OPENAI_KEY,
#         "Content-Type": "application/json"
#     }
#     data = {
#         "messages": [{"role": "system", "content": "Evaluate candidate answers."},
#                      {"role": "user", "content": prompt}],
#         "temperature": 0.5
#     }
#     response = requests.post(url, headers=headers, json=data)
#     return response.json()


