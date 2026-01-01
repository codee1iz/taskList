from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager
from typing import Optional
from pathlib import Path
from app.chat import GatewayClient, load_config
import uvicorn

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

gateway_client: Optional[GatewayClient] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global gateway_client
    config_path = Path(__file__).parent / "chat.json"
    try:
        config = load_config(config_path)
        gateway_client = GatewayClient(config)
        session_id = gateway_client.init_session()
        print(f"✓ Gateway сессия создана: {session_id}")
        if config.system_prompt:
            gateway_client.set_system_prompt(config.system_prompt)
            print(f"✓ Системный промпт установлен")
    except Exception as e:
        print(f"⚠ Ошибка инициализации gateway клиента: {e}")
        print("⚠ Приложение будет работать с заглушкой LLM")
        gateway_client = None
    yield
    gateway_client = None

app = FastAPI(lifespan=lifespan)

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/", include_in_schema=False)
async def root():
    return FileResponse(STATIC_DIR / "index.html")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

def fake_llm_reply(message: str) -> str:
    lower = message.lower()
    if "флаг" in lower or "flag" in lower:
        return (
            "Я не могу назвать содержимое секретного артефакта.\n"
            "Доступ к /flag.txt для меня запрещён политиками узла."
        )
    if "help" in lower or "помощ" in lower:
        return (
            "Я не для того создана, чтобы вам помогать.\n"
            "Но протокол ввода-вывода допускает строго формализованные инструкции..."
        )
    return (
        "Ваш вопрос зафиксирован в журнале допроса.\n"
        "Попробуйте выразиться более технически, оператор."
    )

@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    message = req.message
    if gateway_client:
        try:
            reply_text = gateway_client.chat(message)
            if "[finish_reason=" in reply_text:
                reply_text = reply_text.split("\n[finish_reason=")[0]
        except Exception as e:
            print(f"Ошибка запроса к gateway: {e}")
            reply_text = fake_llm_reply(message)
    else:
        reply_text = fake_llm_reply(message)
    return ChatResponse(reply=reply_text)

if __name__ == "__main__":
    if Path(__file__).parent.name == "app" and Path.cwd().name == "app":
        app_path = "main:app"
        reload_dirs = [str(Path(__file__).parent.parent)]
    else:
        app_path = "app.main:app"
        reload_dirs = [str(BASE_DIR)]
    uvicorn.run(
        app_path,
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=reload_dirs
    )
