# 🔌 Integration Guide for AuraData AI

AuraData is designed to be highly portable. Here is how you can plug it into your existing ecosystem.

## 1. Using AuraData as a Microservice (REST API)
The easiest way is to communicate via HTTP. AuraData exposes a high-level endpoint for autonomous tasks.

- **Endpoint:** `POST /ask`
- **Payload:** `{"query": "Analyze data/my_internal_project_results.csv"}`

```python
# External Python Project Example
import requests

def automate_my_data(task):
    url = "http://localhost:8000/ask"
    res = requests.post(url, json={"query": task})
    return res.json()["data"]["report"]
```

## 2. Using the Shared Data Volume
If your project generates files, simply mount your project's output folder to AuraData's input:

```yaml
# Your docker-compose.yml
services:
  your-app:
    volumes:
      - ./outputs:/shared_data
  auradata:
    volumes:
      - ./outputs:/app/data # Mount your outputs to AuraData's data folder
```

## 3. Direct Module Import (Python)
If you are building a Python app, you can import the core logic directly (once installed):

```python
from core.agent import agent_executor

result = agent_executor.invoke({"task": "Clean users.csv", "iterations": 0})
```
