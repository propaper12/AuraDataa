from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.agent import agent_executor
import json

app = FastAPI(title="AuraData Sentinel SPI", version="0.3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserQuery(BaseModel):
    query: str

@app.get("/")
async def root():
    return {"status": "ok"}

@app.post("/ask")
async def ask_agent(user_query: UserQuery):
    """Basit ve hatasız endpoint."""
    try:
        # Ajanı çalıştır
        result = agent_executor.invoke({"task": user_query.query, "iterations": 0})
        return {"status": "success", "data": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
