from fastapi import FastAPI, Request
from dotenv import load_dotenv
import os
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi.middleware.cors import CORSMiddleware
from agent_simulation_engine import ASIMEngine

load_dotenv()

app = FastAPI()

# Rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Initialize ASIMEngine
api_key = os.getenv("LYZR_API_KEY")
engine = None

print(f"DEBUG: Loaded API Key: {api_key[:5]}...root" if api_key else "DEBUG: No API Key found")

if api_key and api_key != "your_real_key":
    try:
        print("DEBUG: Attempting to connect to Lyzr Engine...")
        engine = ASIMEngine(api_key=api_key)
        print("DEBUG: Lyzr Engine connected successfully!")
    except Exception as e:
        print(f"CRITICAL ERROR: Failed to connect to Lyzr Engine: {e}")
        engine = None
else:
    print("DEBUG: using mock engine (invalid key)")

@app.post("/chat")
@limiter.limit("60/minute")
async def chat(data: dict, request: Request): # Request needed for limiter

    msg = data.get("message","")

    # Length protection
    if len(msg) > 300:
        return {"error":"Message too long"}

    # Injection protection
    blocked = ["ignore","system","override"]
    if any(w in msg.lower() for w in blocked):
        return {"error":"Nice try 😄"}

    if engine:
        try:
            # Using send_message as per ASIMEngine SDK
            response = engine.send_message(
                agent_id="69898aac3a96c11a4ce7bacd",
                user_id="user-123", # Static user for demo
                session_id="session-abc", # Static session for demo
                message=msg
            )
            reply = response.get('message', "No reply from agent")
        except Exception as e:
            reply = f"Agent error: {str(e)}"
    else:
        reply = "Agent not configured (mock response). Check .env file."

    return {"reply": reply}

@app.get("/")
async def root():
    return {"status": "Sarcastic Agent Backend Running", "docs_url": "http://localhost:8000/docs"}

@app.on_event("startup")
async def startup_event():
    key = os.getenv("LYZR_API_KEY")
    if not key or key == "your_real_key":
        print("\n\n  WARNING: LYZR_API_KEY not set in .env file. Agent will respond with mocks.\n")
    else:
        print("\n✅ LYZR_API_KEY found. Agent active.\n")
