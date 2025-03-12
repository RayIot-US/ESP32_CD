import os
import json
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocketDisconnect
from typing import List
app = FastAPI()
# :white_check_mark: Enable CORS for WebSocket support
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Store connected WebSocket clients
clients: List[WebSocket] = []
@app.websocket("/ws")  # :white_check_mark: WebSocket route for ESP32 temperature data
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                parsed_data = json.loads(data)  # Parse JSON from ESP32
                temperature = parsed_data.get("temperature", "N/A")
                print(f":satellite_antenna: Received Temperature Data: {temperature}°C")  # Log data
                # :white_check_mark: Broadcast the temperature data to all connected clients
                for client in clients:
                    await client.send_text(json.dumps({"temperature": temperature}))
            except json.JSONDecodeError:
                print(f":warning: Received non-JSON data: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")
    finally:
        clients.remove(websocket)
# :white_check_mark: Ensure Render uses the correct PORT
if __name__ == "__main__":
    port = int(os.getenv("PORT", "10000"))
    print(f":rocket: Starting WebSocket server on port {port}")
    # :white_check_mark: Start the WebSocket server
    uvicorn.run("server:app", host="0.0.0.0", port=port)
