# import requests

# # Point this to your running server
# URL = "http://localhost:8000/upload_audio/"

# # Path to your local audio file
# local_audio_path = "interview1.mp3"

# # Prepare the form data
# with open(local_audio_path, 'rb') as audio_file:
#     files = {
#         'file': ('interview1.mp3', audio_file, 'audio/mp3')
#     }
#     data = {
#         'session_id': 'test-session-123',
#         'current_question': 'Tell me about polymorphism.'
#     }

#     response = requests.post(URL, data=data, files=files)

# print("Response from Server:")
# print(response.json())


import requests

url = "http://localhost:8000/upload/"
# url = "https://talentscout-production.up.railway.app/upload/"

session_id = "session-456"
file_path = "interview1.mp3"

# with open(file_path, "rb") as f:
#     files = {"audio_file": (file_path, f, "audio/mp3")}
#     data = {"session_id": "test-session-123"}
#     response = requests.post(url, files=files, data=data)
with open(file_path, "rb") as f:
    files = {"audio_file": (file_path, f, "audio/wav")}
    params = {"session_id": session_id}  # <-- Send as query param
    response = requests.post(url, params=params, files=files)

print(response.json())
print(response.json())
