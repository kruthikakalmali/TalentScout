# from fastapi import WebSocket
# from app.session import update_session
# from app.azure_client import create_speech_recognizer

# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     session_id = websocket.query_params["session_id"]
    
#     recognizer = create_speech_recognizer()

#     while True:
#         data = await websocket.receive_bytes()
#         # Here you should feed data chunks into Azure Speech SDK (customized streaming)
#         # For simplicity, assume you get full transcript after some time
#         text_result = "fake-transcript"  # replace with real Azure result
        
#         await update_session(session_id, "last_transcript", text_result)
#         await websocket.send_text(text_result)
