import os
import json
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI(lifespan="on")  # Ensures long-lived WebSocket connections

# ✅ Enable CORS for WebSocket Support
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clients: List[WebSocket] = []

@app.websocket("/ws")  # ✅ WebSocket route for ESP32 & WebSocket King
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    print("✅ WebSocket Client Connected!")

    try:
        while True:
            data = await websocket.receive_text()  # Receive WebSocket message
            print(f"📡 Received Data: {data}")  # Log received data

            # ✅ Send acknowledgment back to sender
            await websocket.send_text(f"Server received: {data}")

            # ✅ Broadcast the message to all connected clients
            for client in clients:
                await client.send_text(data)

    except Exception as e:
        print(f"❌ WebSocket Error: {e}")
    finally:
        clients.remove(websocket)
        print("❌ WebSocket Client Disconnected!")

# ✅ Start WebSocket Server with Daphne Compatibility
if __name__ == "__main__":
    port = int(os.getenv("PORT", "10000"))
    print(f"🚀 Starting WebSocket server on port {port}")
    uvicorn.run("server:app", host="0.0.0.0", port=port, ws_ping_interval=20, ws_ping_timeout=30)



# import os
# import json
# import uvicorn
# from fastapi import FastAPI, WebSocket
# from fastapi.middleware.cors import CORSMiddleware
# from typing import List

# app = FastAPI()

# # ✅ Enable CORS for WebSocket Support
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# clients: List[WebSocket] = []

# @app.websocket("/ws")  # ✅ WebSocket route for ESP32 & WebSocket King
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     clients.append(websocket)
#     print("✅ WebSocket Client Connected!")

#     try:
#         while True:
#             data = await websocket.receive_text()  # Receive WebSocket message
#             print(f"📡 Received Data: {data}")  # Log received data

#             # ✅ Send acknowledgment back to sender
#             await websocket.send_text(f"Server received: {data}")

#             # ✅ Broadcast the message to all connected clients
#             for client in clients:
#                 await client.send_text(data)

#     except Exception as e:
#         print(f"❌ WebSocket Error: {e}")
#     finally:
#         clients.remove(websocket)
#         print("❌ WebSocket Client Disconnected!")

# # ✅ Start WebSocket Server
# if __name__ == "__main__":
#     port = int(os.getenv("PORT", "10000"))
#     print(f"🚀 Starting WebSocket server on port {port}")
#     uvicorn.run("server:app", host="0.0.0.0", port=port)



# # import os
# # import json
# # import uvicorn
# # from fastapi import FastAPI, WebSocket
# # from fastapi.middleware.cors import CORSMiddleware
# # from typing import List

# # app = FastAPI()

# # # ✅ Enable CORS for WebSocket support
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["*"],
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # clients: List[WebSocket] = []

# # @app.websocket("/ws")  # ✅ WebSocket route for ESP32 temperature data
# # async def websocket_endpoint(websocket: WebSocket):
# #     await websocket.accept()
# #     clients.append(websocket)
# #     try:
# #         while True:
# #             data = await websocket.receive_text()
# #             parsed_data = json.loads(data)  # Parse JSON from ESP32
# #             ambient_temp = parsed_data.get("ambient_temp", "N/A")
# #             object_temp = parsed_data.get("object_temp", "N/A")
# #             print(f"📡 Received Temperature Data: Ambient: {ambient_temp}°C, Object: {object_temp}°C")

# #             # ✅ Broadcast temperature data to all connected clients
# #             for client in clients:
# #                 await client.send_text(json.dumps(parsed_data))

# #     except Exception as e:
# #         print(f"Connection closed: {e}")
# #     finally:
# #         clients.remove(websocket)

# # # ✅ Start WebSocket Server
# # if __name__ == "__main__":
# #     port = int(os.getenv("PORT", "10000"))
# #     print(f"🚀 Starting WebSocket server on port {port}")
# #     uvicorn.run("server:app", host="0.0.0.0", port=port)


# # # import os
# # # import json
# # # import uvicorn
# # # from fastapi import FastAPI, WebSocket
# # # from fastapi.middleware.cors import CORSMiddleware
# # # from starlette.websockets import WebSocketDisconnect
# # # from typing import List
# # # app = FastAPI()
# # # # :white_check_mark: Enable CORS for WebSocket support
# # # app.add_middleware(
# # #     CORSMiddleware,
# # #     allow_origins=["*"],
# # #     allow_credentials=True,
# # #     allow_methods=["*"],
# # #     allow_headers=["*"],
# # # )
# # # # Store connected WebSocket clients
# # # clients: List[WebSocket] = []
# # # @app.websocket("/ws")  # :white_check_mark: WebSocket route for ESP32 temperature data
# # # async def websocket_endpoint(websocket: WebSocket):
# # #     await websocket.accept()
# # #     clients.append(websocket)
# # #     try:
# # #         while True:
# # #             data = await websocket.receive_text()
# # #             try:
# # #                 parsed_data = json.loads(data)  # Parse JSON from ESP32
# # #                 temperature = parsed_data.get("temperature", "N/A")
# # #                 print(f":satellite_antenna: Received Temperature Data: {temperature}°C")  # Log data
# # #                 # :white_check_mark: Broadcast the temperature data to all connected clients
# # #                 for client in clients:
# # #                     await client.send_text(json.dumps({"temperature": temperature}))
# # #             except json.JSONDecodeError:
# # #                 print(f":warning: Received non-JSON data: {data}")
# # #     except WebSocketDisconnect:
# # #         print("Client disconnected")
# # #     finally:
# # #         clients.remove(websocket)
# # # # :white_check_mark: Ensure Render uses the correct PORT
# # # if __name__ == "__main__":
# # #     port = int(os.getenv("PORT", "10000"))
# # #     print(f":rocket: Starting WebSocket server on port {port}")
# # #     # :white_check_mark: Start the WebSocket server
# # #     uvicorn.run("server:app", host="0.0.0.0", port=port)
