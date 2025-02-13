from fastapi import FastAPI, WebSocket, Request
from db import messages_db
from routes import routes

db = messages_db.db()
db.setup_db()

app = FastAPI()

app = routes.add_routes(app, db)

