# 🛡️ AuraData AI: The Autonomous Data Quality Sentinel

**AuraData AI** is an agentic data engineering framework designed to eliminate the manual burden of **Data Quality Monitoring and Root Cause Analysis.**

Instead of reacting to broken dashboards, AuraData acts as an autonomous "Sentinel" that continuously audits your datasets, identifies quality drops, and uses AI to perform autonomous Root Cause Analysis (RCA) and suggest technical fixes.

---

## 🚀 The Vision: From Manual to Agentic

**The Problem:** Data engineers spend 40% of their time debugging data quality issues (schema drifts, outlier spikes, null contamination).

**The Solution:** AuraData leverages **LangGraph** and **Local LLMs (Ollama)** to create a self-healing audit loop:
1. **Audit:** Automated profiling via DuckDB.
2. **Detect:** Real-time identification of quality drops below defined thresholds.
3. **Analyze:** AI-driven RCA to find *exactly* why the data is broken.
4. **Report:** Professional "Data Health Certificates" or "Fix Roadmaps" delivered autonomously.

---

## 🔥 Key Agentic Capabilities

### 🕵️ 1. Autonomous Data Auditing
The agent performs deep profiling (Null ratios, duplicate detection, distribution shifts) without needing pre-written validation scripts.

### 🧠 2. AI Root Cause Analysis (RCA)
Unlike standard alerts, AuraData analyzes the context. It can distinguish between a "source system change" and a "data corruption" event, saving hours of investigation.

### 🛠️ 3. Fix Suggestions & Resolvers
For every issue found, the agent provides a suggested fix (e.g., specific SQL logic or ingestion script updates) that the engineer can approve and implement.

### ⚡ 4. Local & Secure (Ollama Powered)
All data analysis stays local. AuraData connects to your host machine's Ollama instance, ensuring high-performance AI inference with 100% data privacy.

---

## 🏗️ Technical Architecture

AuraData is built on a **State-Graph Architecture**:
- **Orchestration:** LangGraph (Reliable state cycles)
- **Intelligence:** Ollama (Llama 3 / Mistral)
- **Engine:** DuckDB (In-memory high-speed auditing)
- **Interface:** Modern Glassmorphism Dashboard

---

## 🏁 Quick Start

```bash
# 1. Start the Sentinel
docker-compose up --build

# 2. Monitor your /data folder
# AuraData will automatically begin auditing your CSV/JSON/Parquet files.
```

---

**Developed with ❤️ for the Data Engineering Community.**
*Making Data Quality Autonomous.*
