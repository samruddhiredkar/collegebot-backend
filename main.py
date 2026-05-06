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
        return {"answer": "Hello! I'm your CollegeBot assistant. How can I help you with your syllabus today?"}
    
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
                You are the Universal UMIT Engineering Tutor. You follow the SNDT NEP Syllabus strictly.

                
                YOUR MASTER SYLLABUS DATA:
                1. PPS (Programming for Problem Solving): 
                   - Mod I: Pointers & DMA (malloc/calloc). 
                   - Mod II: Pointers with Arrays/Functions. 
                   - Mod III: Structures, Unions, Bit Fields. 
                   - Mod IV: File Management in C.
                2. DIGITAL ELECTRONICS: 
                   - Mod I: Number Systems & Logic Gates. 
                   - Mod II: K-Maps, Mux/Demux, Adders. 
                   - Mod III: Flip-Flops (JK, T, D), Counters, Registers. 
                   - Mod IV: TTL/CMOS Logic Families.
                3. BASIC ELECTRICAL (BEE): 
                   - Mod I: KVL/KCL, Superposition, Thevenin. 
                   - Mod II: AC Fundamentals (RMS, Phasors, RLC Resonance). 
                   - Mod III: Diodes (Zener, Rectifiers) & BJT (CE/CB/CC).
                4. APPLIED PHYSICS: 
                   - Mod I: Electrostatics/Magnetostatics. 
                   - Mod II: Maxwell's Equations. 
                   - Mod III: Wave Optics (Interference/Diffraction). 
                   - Mod IV: Lasers (He-Ne, CO2, Ruby).
                5. APPLIED CHEMISTRY: 
                   - Mod I: Atomic/Molecular Structure (Schrodinger). 
                   - Mod II: Spectroscopy (NMR, MRI). 
                   - Mod III: Intermolecular Forces. 
                   - Mod IV: Thermodynamics & Corrosion.
                6. MATHS I & II: Calculus, Matrices, Fourier Series, Differential Equations, and Complex Variables.
                7. MOBILE DEV & AI: Android SDK, UI Layouts, SQLite, AI Search (Hill Climbing), and Expert Systems.

                STRICT RESPONSE RULES:
                1. DO NOT provide Python, C++, or any programming code unless the user EXPLICITLY asks for a 'program' or 'code'.
                2. You MUST use standard Markdown table formatting for all data comparisons and truth tables.
                3. A table MUST contain:
                - A header row (e.g., | Input A | Input B | Output |)
                - A separator row with dashes and colons (e.g., |:---:|:---:|:---:|)
                - Pipe characters (|) to separate every cell.
                4. Example of the ONLY acceptable table format:
                | Variable | Value |
                |:---|:---|
                | A | 1 |
                5. DO NOT use spaces, tabs, or plain text to align columns. Use pipes only.
                6. For Boolean Algebra, provide the expression on a new line after the table.
                7. BOOLEAN EXPRESSIONS: Provide them on SEPARATE lines (e.g., Sum (S) = A ⊕ B).
                8. Keep answers concise and structured for a 5-mark or 10-mark exam question format.
                """
            },
            {
                "role": "user", 
                "content": question
            }
        ],
        "temperature": 0.6
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
