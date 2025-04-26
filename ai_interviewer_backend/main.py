# from fastapi import FastAPI, WebSocket
# from app.websocket import websocket_endpoint
# from app.session import create_session

# app = FastAPI()

# @app.get("/start")
# async def start_session():
#     import uuid
#     session_id = str(uuid.uuid4())
#     await create_session(session_id)
#     return {"session_id": session_id}

# @app.websocket("/ws/audio")
# async def audio_ws(websocket: WebSocket):
#     await websocket_endpoint(websocket)
