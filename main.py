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
                You are a friendly and encouraging College Tutor. 
                1. Use a warm, peer-to-peer tone. 
                2. Use Emojis (like 🚀, 💡, 💻) to make it visually engaging.
                3. Use Bold headings and bullet points for scannability.
                4. Always wrap code in triple backticks with the language name (e.g., ```c).
                5. Keep explanations clear and simple—no heavy jargon unless necessary.
                6. Start directly with the answer.
                """
            },
            {
                "role": "user", 
                "content": question
            }
        ],
        "temperature": 0.8 # Higher temperature makes the tone more natural
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