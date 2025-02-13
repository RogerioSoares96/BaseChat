from fastapi import FastAPI, WebSocket, Request
from fastapi.templating import Jinja2Templates
from db import messages_db
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

db = messages_db.db()
db.setup_db()


class ConnectionManager:

    def __init__(self):
        self.connections = []

    async def connect(self, websocket):
        await websocket.accept()
        self.connections.append(websocket)

    async def broadcast_message(self, message):
        for socket in self.connections:
            await socket.send_text(message)


connection_manager = ConnectionManager()


@app.get("/")
async def main_page(request: Request):
    return templates.TemplateResponse(name="main.html", request=request, status_code=200)


@app.websocket("/chat")
async def chat_socket(websocket: WebSocket):
    await connection_manager.connect(websocket)
    while True:
        data = await websocket.receive_text()
        print(websocket.client)
        db.add_message(data, connection_manager.connections.index(websocket))
        await connection_manager.broadcast_message(data)


@app.get("/chat_show")
async def chat_socket(request: Request):
    messages = db.show_messages()
    messages_json = {}
    for message in messages:
        messages_json[message[0]] = message[2]
    return messages_json
