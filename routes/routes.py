from fastapi import WebSocket, Request
from fastapi.templating import Jinja2Templates
from ws_connection_manager import ConnectionManager

connection_manager = ConnectionManager()

templates = Jinja2Templates(directory="templates")


def add_routes(app, db):

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

    return app