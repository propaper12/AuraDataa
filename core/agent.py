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
from utils.reporter import reporter
from apscheduler.schedulers.background import BackgroundScheduler

# 1. Düğüm: Otonom Denetçi (Sentinel Audit)
def audit_node(state: AgentState):
    task = state.get('task', 'kafka://market_data').lower()
    print(f"--- SENTINEL AUDIT: Identifying target {task} ---")
    
    # Eklenti (Plugin) Seçimi
    if task.startswith("kafka://"):
        topic = task.replace("kafka://", "")
        connector = CONNECTOR_HUB["kafka"]
        samples = connector.fetch_sample(topic)
        
        if not samples:
            audit_results = {"error": "Kafka stream is empty or unreachable", "quality_score": 0, "status": "Failed"}
        else:
            # Otonom Kalite Ölçümü
            null_counts = {}
            total_fields = 0
            for msg in samples:
                for k, v in msg.items():
                    total_fields += 1
                    if v is None or v == "":
                        null_counts[k] = null_counts.get(k, 0) + 1
            
            avg_null_rate = (sum(null_counts.values()) / total_fields) if total_fields > 0 else 0
            quality_score = max(0, 1.0 - (avg_null_rate * 5))
            audit_results = {"quality_score": quality_score, "null_rates": null_counts}
    elif task.startswith("sql://"):
        connector = CONNECTOR_HUB["sql"]
        connector.connect(task.replace("sql://", ""))
        audit_results = {"quality_score": 0.88, "null_rates": {"db_records": 0.05}}
    else:
        # Standart dosya eklentisi (DuckDB)
        audit_results = auditor.audit_file(task)

    if "error" in audit_results:
        return {
            "error": audit_results.get("error", "Unknown Audit Error"), 
            "quality_score": 0.0, 
            "quality_metrics": {}, 
            "issue_found": True,
            "iterations": (state.get("iterations") or 0) + 1
        }

    return {
        "quality_metrics": audit_results.get("null_rates", {}),
        "quality_score": audit_results.get("quality_score", 0.0),
        "issue_found": audit_results.get("quality_score", 1.0) < 0.85,
        "error": "",
        "iterations": (state.get("iterations") or 0) + 1
    }

# 2. Düğüm: Kök Neden Analisti (RCA Node)
def rca_node(state: AgentState):
    print("--- ANALYSIS STARTED: Calling Ollama ---")
    if not state.get("issue_found", False):
        return {"analysis": "Quality is stable. No action required.", "fix_suggestion": "None"}
    
    prompt = f"""
    CONTEXT: Quality Score 1.0 is PERFECT, 0.0 is CRITICAL FAILURE.
    Current Data Status:
    - Quality Score: {state.get('quality_score', 0.0)} (Scale: 0-1)
    - Detailed Issues: {state.get('quality_metrics', {})}
    - Error Logs: {state.get('error', 'None')}
    
    TASK: If score is less than 0.85, analyze WHY and provide a REALISTIC data engineering fix.
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
    status = "⚠️ ALERT" if state.get("issue_found", True) else "✅ STABLE"
    
    report_prompt = f"""
    Systems Status: {status}
    Quality Score: {state.get('quality_score', 0.0)}
    Analysis: {state.get('analysis', 'No analysis available.')}
    Fix Suggestion: {state.get('fix_suggestion', 'Check system logs.')}
    Generate a professional data engineering sentinel report.
    """
    response = llm.invoke(report_prompt)
    return {"report": response.content}

# 4. Düğüm: Teslimat (PDF & Email)
def delivery_node(state: AgentState):
    print("--- DELIVERY: Archiving PDF and Dispatching Reports ---")
    filepath = reporter.generate_pdf(state)
    reporter.send_email(filepath, state)
    return {"report": state['report'] + f"\n\n[FILE ARCHIVED]: {filepath}"}

# AuraData Sentinel Workflow
def aura_agent():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("audit", audit_node)
    workflow.add_node("analyze", rca_node)
    workflow.add_node("report", reporter_node)
    workflow.add_node("delivery", delivery_node)
    
    workflow.set_entry_point("audit")
    workflow.add_edge("audit", "analyze")
    workflow.add_edge("analyze", "report")
    workflow.add_edge("report", "delivery")
    workflow.add_edge("delivery", END)
    
    return workflow.compile()

agent_executor = aura_agent()

# Otonom Zamanlayıcı (Her 10 dakikada bir çalışır)
def run_autonomous_audit():
    print("🚀 Running Autonomous Scheduled Audit...")
    # Varsayılan olarak Kafka market_data topic'ine bakabilir
    agent_executor.invoke({"task": "kafka://market_data", "iterations": 0})

scheduler = BackgroundScheduler()
# Her 10 dakikada bir otomatik denetim başlat
scheduler.add_job(run_autonomous_audit, 'interval', minutes=10)
scheduler.start()
