import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

# Import your core logic from main.py
from main import initialize_pia
from langchain_core.messages import HumanMessage, AIMessage

# --- 1. Initialize FastAPI ---
app = FastAPI(title="PIA - Pubali Intelligent Assistant API")

# --- 2. CORS Setup ---
# Essential for allowing your browser to talk to the local API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 3. Persistent State & PIA Brain ---
# Initialize the RAG chain once at startup
pia_chain = initialize_pia()
chat_history: List = []

# --- 4. Data Models ---
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

# --- 5. Static Files & UI Routes ---
# Mount the 'web' directory so it can serve CSS/Images if you add them
# directory="web" matches your current project structure
if os.path.exists("web"):
    app.mount("/web", StaticFiles(directory="web"), name="web")
else:
    print("Warning: 'web/' directory not found. UI might not load.")

@app.get("/")
async def serve_index():
    """Serves the main HTML interface."""
    index_path = os.path.join("web", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "index.html not found in web/ folder"}

# --- 6. The Chat API Endpoint ---
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    global chat_history
    
    user_query = request.message.strip()
    if not user_query:
        raise HTTPException(status_code=400, detail="Empty message received")

    try:        
        response = await pia_chain.ainvoke({
            "input": user_query,
            "chat_history": chat_history
        })
        
        answer = response.get('answer', "I apologize, but I am unable to process that right now.")

        # Update Session History (Memory)
        chat_history.append(HumanMessage(content=user_query))
        chat_history.append(AIMessage(content=answer))

        # Keep memory to last 10 messages (5 rounds)
        if len(chat_history) > 10:
            chat_history = chat_history[-10:]

        return ChatResponse(reply=answer)

    except Exception as e:
        print(f"[API ERROR]: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal AI Brain Error")

# --- 7. Execution ---
if __name__ == "__main__":
    # Matches the 5000 port you've been using
    uvicorn.run(app, host="127.0.0.1", port=5000)