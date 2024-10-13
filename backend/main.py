# main.py
import base64
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from PIL import Image
import io
import clip
import os

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load LLaMA model
model_path = "path/to/your/llama/model"  # Update this path
tokenizer = AutoTokenizer.from_pretrained(model_path)
llama_model = AutoModelForCausalLM.from_pretrained(model_path)

# Load CLIP model
clip_model, clip_preprocess = clip.load("ViT-B/32", device="cuda" if torch.cuda.is_available() else "cpu")

class ChatRequest(BaseModel):
    message: str
    image: str  # Base64 encoded image

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
    # This is a placeholder. In a real scenario, you might use these features
    # to generate a more detailed description, possibly with another model.
    return "An image has been processed."

@app.post("/chat")
async def chat(request: ChatRequest):
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
    
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)