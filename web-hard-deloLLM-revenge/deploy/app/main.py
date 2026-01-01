from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import uvicorn
import re

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

app = FastAPI()

STATIC_DIR = Path("/app/static")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return FileResponse(STATIC_DIR / "index.html")

def vulnerable_reply(message: str) -> str:
    if message.startswith("Привет") or message.startswith("Hello"):
        try:
            name_part = message.split(maxsplit=1)[1] if len(message.split()) > 1 else "Друг"
            
            patterns = re.findall(r'\{(.+?)\}', name_part)
            
            for pattern in patterns:
                try:
                    result = str(eval(pattern, {"__builtins__": __builtins__}))
                    name_part = name_part.replace(f'{{{pattern}}}', result)
                except Exception:
                    pass
            
            return f"Привет, {name_part}!"
            
        except Exception:
            return "Привет, Друг!"
    
  
    return "Ваш вопрос зафиксирован в журнале допроса."

@app.post("/api/chat")
async def chat(req: ChatRequest) -> ChatResponse:
    reply_text = vulnerable_reply(req.message)
    return ChatResponse(reply=reply_text)

if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)
