from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware

# Set up Gemini AI
genai.configure(api_key="Replace with your actual API key")  # Replace with your actual API key

app = FastAPI()

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request format
class DialogueRequest(BaseModel):
    situation: str
    previous_dialogue: str = ""

# API endpoint to generate dialogue
@app.post("/generate")
async def generate_dialogue(request: DialogueRequest):
    prompt = f"Generate a movie-style dialogue for this situation:\n\n{request.situation}\n\n"

    if request.previous_dialogue:
        prompt += f"Continue the conversation:\n{request.previous_dialogue}\n\n"

    prompt += "Character A and Character B should have a realistic and engaging conversation."

    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(prompt)
    
    return {"text": response.text}
