from fastapi import FastAPI
from pydantic import BaseModel

from .agent import PulseCXAgent

app = FastAPI(title="PulseCX Assistant", version="0.1.0")

# Initialise agent once per process
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
    """
    Main chat endpoint for the hyper-personalized assistant.
    """
    result = agent.handle_message(
        user_id=request.user_id,
        message=request.message,
        lat=request.location.lat,
        lon=request.location.lon,
    )
    return ChatResponse(**result)
