class ConnectionManager:

    def __init__(self):
        self.connections = []

    async def connect(self, websocket):
        await websocket.accept()
        self.connections.append(websocket)

    async def broadcast_message(self, message):
        for socket in self.connections:
            await socket.send_text(message)