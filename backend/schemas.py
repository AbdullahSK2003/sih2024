from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    image: str  # Base64 encoded image

class ChatResponse(BaseModel):
    response: str