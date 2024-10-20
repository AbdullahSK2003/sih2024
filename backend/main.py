from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
import base64
from PIL import Image
import io
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import clip

from database import SessionLocal, engine
import models
from schemas import ChatRequest, ChatResponse

app = FastAPI()

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Load LLaMA model
model_path = os.getenv("LLAMA_MODEL_PATH")
tokenizer = AutoTokenizer.from_pretrained(model_path)
llama_model = AutoModelForCausalLM.from_pretrained(model_path)

# Load CLIP model
clip_model, clip_preprocess = clip.load("ViT-B/32", device="cuda" if torch.cuda.is_available() else "cpu")

def generate_llama_response(prompt, max_length=100):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = llama_model.generate(**inputs, max_length=max_length)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def process_image_with_clip(image):
    image_input = clip_preprocess(image).unsqueeze(0)
    with torch.no_grad():
        image_features = clip_model.encode_image(image_input)
    return image_features

def generate_image_description(image_features):
    # Placeholder: In a real scenario, you'd use these features to generate a description
    return "An image has been processed."

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    # Decode base64 image
    image_data = base64.b64decode(request.image.split(',')[1])
    image = Image.open(io.BytesIO(image_data))
    
    # Process image with CLIP
    image_features = process_image_with_clip(image)
    
    # Generate image description
    image_description = generate_image_description(image_features)
    
    # Generate response using LLaMA
    prompt = f"Image description: {image_description}\nUser: {request.message}\nAI:"
    response = generate_llama_response(prompt)
    
    # Store chat in database
    db_chat = models.Chat(user_message=request.message, ai_response=response)
    db.add(db_chat)
    db.commit()
    
    return ChatResponse(response=response)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    # Here you would typically save the file to a cloud storage service
    # For this example, we'll just return a dummy URL
    return {"url": f"https://example.com/images/{file.filename}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))