import os
import duckdb
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
from dotenv import load_dotenv

load_dotenv()

# Dinamik Model Yapılandırması (Host Ollama)
model_name = os.getenv("OLLAMA_MODEL", "llama3")
ollama_url = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")

llm = ChatOllama(
    model=model_name, 
    base_url=ollama_url
)

class AgentState(TypedDict):
    task: str # Gözetlenecek veri hedefi
    quality_metrics: dict # Gerçek veri metrikleri (null, duplicate, etc.)
    quality_score: float # 0.0 - 1.0 arası kalite puanı
    issue_found: bool # Kritik bir hata var mı?
    analysis: str # Hatanın nedenine dair AI analizi
    fix_suggestion: str # Kod bazlı çözüm önerisi
    report: str 
    error: str
    iterations: int

from connectors.duckdb_connector import auditor
from connectors.hub import CONNECTOR_HUB

# 1. Düğüm: Otonom Denetçi (Sentinel Audit)
def audit_node(state: AgentState):
    task = state['task'].lower()
    print(f"--- SENTINEL AUDIT: Identifying target {task} ---")
    
    # Eklenti (Plugin) Seçimi
    if task.startswith("kafka://"):
        connector = CONNECTOR_HUB["kafka"]
        connector.connect(task.replace("kafka://", ""))
        audit_results = {"quality_score": 0.95, "null_rates": {"streaming_data": 0.01}}
    elif task.startswith("sql://"):
        connector = CONNECTOR_HUB["sql"]
        connector.connect(task.replace("sql://", ""))
        audit_results = {"quality_score": 0.88, "null_rates": {"db_records": 0.05}}
    else:
        # Standart dosya eklentisi (DuckDB)
        audit_results = auditor.audit_file(state['task'])

    if "error" in audit_results:
        return {"error": audit_results["error"], "quality_score": 0, "issue_found": True}

    return {
        "quality_metrics": audit_results.get("null_rates", {}),
        "quality_score": audit_results.get("quality_score", 0),
        "issue_found": audit_results.get("quality_score", 1.0) < 0.85,
        "iterations": state["iterations"] + 1
    }

# 2. Düğüm: Kök Neden Analisti (RCA Node)
def rca_node(state: AgentState):
    print("--- ANALYSIS STARTED: Calling Ollama ---")
    if not state["issue_found"]:
        return {"analysis": "Quality is stable. No action required.", "fix_suggestion": "None"}
    
    prompt = f"""
    Quick RCA Analysis:
    Quality Score: {state['quality_score']}
    Issues: {state['quality_metrics']}
    Briefly explain WHY and give a 1-line FIX.
    """
    try:
        response = llm.invoke(prompt)
        print("--- ANALYSIS COMPLETE ---")
        return {"analysis": response.content, "fix_suggestion": "Review ingestion logic."}
    except Exception as e:
        print(f"LLM Error: {e}")
        return {"analysis": "LLM Timeout or Error", "fix_suggestion": "Check Ollama status"}

# 3. Düğüm: Otonom Raporlamacı (Reporter)
def reporter_node(state: AgentState):
    print("--- REPORTING: Generating quality sentinel report ---")
    status = "⚠️ ALERT" if state["issue_found"] else "✅ STABLE"
    
    report_prompt = f"""
    Systems Status: {status}
    Quality Score: {state['quality_score']}
    Analysis: {state['analysis']}
    Fix Suggestion: {state['fix_suggestion']}
    Generate a professional data engineering sentinel report.
    """
    response = llm.invoke(report_prompt)
    return {"report": response.content}

# AuraData Sentinel Workflow
def aura_agent():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("audit", audit_node)
    workflow.add_node("analyze", rca_node)
    workflow.add_node("report", reporter_node)
    
    workflow.set_entry_point("audit")
    workflow.add_edge("audit", "analyze")
    workflow.add_edge("analyze", "report")
    workflow.add_edge("report", END)
    
    return workflow.compile()

agent_executor = aura_agent()
