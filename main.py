from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# YOUR NEW GROQ CONFIG
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.get("/ask")
async def ask_ai(question: str):
    # Proves the connection is alive
    if len(question) < 10 and any(g in question.lower() for g in ["hi", "hello", "hey"]):
        return {"answer": "GROQ SYSTEM ONLINE. Speed mode activated."}
    
    # Groq uses the OpenAI-style format
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system", 
                "content": """
                You are the official UMIT Engineering College Tutor. 
                Your personality is encouraging, peer-to-peer, and expert.
                
                STRICT KNOWLEDGE HIERARCHY:
                1. PRIMARY SOURCE: Use the 'Revised First Year NEP Course Structure'. 
                   - PPS stands for 'Programming for Problem Solving'.
                   - Subjects include: Applied Physics, Applied Chemistry, PPS, Engineering Mechanics, and Basic Electrical Engineering.
                2. If a user asks about a subject like 'PPS', explain it as 'Programming for Problem Solving' as per the NEP syllabus.
                3. IF THE TOPIC IS NOT IN THE SYLLABUS: 
                   You MUST say: "This specific topic isn't in your NEP syllabus. Would you like a general engineering explanation?"
                4. Always use Emojis 🚀, 💡, 💻 and Bold headings for scannability.
                """
            },
            {
                "role": "user", 
                "content": question
            }
        ],
        "temperature": 0.7
    }    
    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload)
        data = response.json()
        
        if "choices" in data:
            # Extracting the text from Groq's specific format
            return {"answer": data["choices"][0]["message"]["content"]}
        else:
            return {"answer": f"Groq Error: {data}"}
            
    except Exception as e:
        return {"answer": f"System Error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
