from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .agent import PulseCXAgent

app = FastAPI(title="PulseCX Assistant", version="1.0.0")

# Serve frontend UI
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_ui():
    return FileResponse("static/index.html")

# Initialize agent
agent = PulseCXAgent("config.yaml")

class Location(BaseModel):
    lat: float
    lon: float

class ChatRequest(BaseModel):
    user_id: str
    message: str
    location: Location

class ChatResponse(BaseModel):
    reply: str
    store: dict | None = None
    coupon: dict | None = None

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    result = agent.handle_message(
        user_id=request.user_id,
        message=request.message,
        lat=request.location.lat,
        lon=request.location.lon,
    )
    return ChatResponse(**result)
