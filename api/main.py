from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from core.agent import agent_executor
import os

app = FastAPI(title="AuraData Sentinel SPI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserQuery(BaseModel):
    query: str

# 1. API Endpoint
@app.post("/ask")
async def ask_agent(user_query: UserQuery):
    try:
        result = agent_executor.invoke({"task": user_query.query, "iterations": 0})
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 2. UI (HTML) Sunumu
if os.path.exists("web"):
    app.mount("/web", StaticFiles(directory="web"), name="web")

# 3. Rapor Yönetimi
if os.path.exists("reports"):
    app.mount("/download", StaticFiles(directory="reports"), name="download")

@app.get("/reports")
async def list_reports():
    """Arşivlenmiş PDF raporlarını listeler."""
    try:
        files = os.listdir("reports")
        reports = [f for f in files if f.endswith(".pdf")]
        reports.sort(reverse=True) # En yeniler üstte
        return {"status": "success", "reports": reports}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/")
async def read_index():
    return FileResponse('web/index.html')
