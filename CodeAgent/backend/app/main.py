from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
from .agent_runner import run_agent

app = FastAPI(title="Code Generation Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
async def serve_index():
    return FileResponse(STATIC_DIR / "index.html")


class AgentRequest(BaseModel):
    api_key: str
    user_prompt: str
    workspace: str = r"C:\Users\GenAICHNKPRUSR04\Documents\CodeAgent\generated"
    base_url: str = "https://genailab.tcs.in/v1"
    model: str = "genailab-maas-gpt-5.2-codex"


@app.post("/api/agent/run")
async def api_run_agent(payload: AgentRequest):
    return StreamingResponse(
        run_agent(
            api_key=payload.api_key,
            user_prompt=payload.user_prompt,
            workspace=payload.workspace,
            base_url=payload.base_url,
            model=payload.model,
        ),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
