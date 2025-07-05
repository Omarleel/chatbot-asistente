from fastapi import FastAPI, Request
from api.routes import auth_routes, chat_routes

app = FastAPI(
    title="chatbot-asistente"
)

app.include_router(auth_routes.router, prefix="/auth")
app.include_router(chat_routes.router, prefix="/chat")