# 🤖 Structured AI Log Analysis System with Python & LLMs (Agentic Copilot Approach)

## 🧠 Overview: Copilot-Style Agentic System

This system uses an **agentic architecture** to operate like a log analysis copilot. It:

- Ingests and understands logs
- Parses and structures them
- Detects anomalies
- Interacts with users conversationally
- Autonomously recommends actions or triage

Each module acts as a specialized **agent** in a multi-agent environment coordinated by a central **controller agent**.

```
┌────────────┐     ┌────────────┐     ┌─────────────┐     ┌────────────┐     ┌────────────┐
│  Log Source│ ──▶ │  Ingestor  │ ──▶ │  Parser Agent│ ──▶ │ Analyzer Agent │ ──▶ │ UX Agent   │
└────────────┘     └────────────┘     └─────────────┘     └────────────┘     └────────────┘
                                  ↓            ↓               ↓
                       Storage Agent     Insight Agent    Copilot Interaction
```

---

## 🗂️ Input Types

- System logs (e.g., `/var/log/`)
- Application logs (JSON, plain text, XML)
- Cloud logs (AWS CloudTrail, Azure Monitor, GCP Logs)
- Security logs (Sysmon, Sentinel, SIEM)

---

## ⚙️ Agents & Responsibilities

### 🟡 1. **Ingestor Agent**

Fetches logs from filesystem, APIs, or cloud streams.

```python
class IngestorAgent:
    def read_logs(self, log_path: str) -> list[str]:
        import os
        logs = []
        for filename in os.listdir(log_path):
            with open(os.path.join(log_path, filename), 'r') as f:
                logs.extend(f.readlines())
        return logs
```

### 🟡 2. **Parser Agent**

Parses and structures logs.

```python
class ParserAgent:
    def parse_line(self, line: str) -> dict:
        import re
        pattern = r'(?P<ip>[\d\.]+) - - \[(?P<timestamp>.*?)\] "(?P<method>\w+) (?P<url>\S+)'
        match = re.match(pattern, line)
        return match.groupdict() if match else {"raw": line}
```

### 🟡 3. **Storage Agent**

Converts parsed data into structured format (Pandas, DuckDB, or SQL).

```python
class StorageAgent:
    def store(self, parsed_logs: list[dict]):
        import pandas as pd
        return pd.DataFrame(parsed_logs)
```

### 🟡 4. **Analyzer Agent (LLM Copilot)**

Uses GPT-4 or other LLMs to detect anomalies and summarize.

```python
class AnalyzerAgent:
    def __init__(self, openai_client):
        self.client = openai_client

    def analyze(self, logs: list[str], task: str) -> str:
        prompt = f"{task}\n\nLogs:\n{logs[:100]}"
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
```

### 🟡 5. **Insight Agent**

Extracts actionable insights, trends, and flags for human-in-the-loop review.

### 🟡 6. **UX Agent (Chat UI)**

- Streamlit or Gradio based interface
- Accepts natural language queries
- Shows visual summaries and logs

---

## 🔍 Natural Language Log Querying

- “Show all 500 errors in the last hour”
- “Summarize failed login attempts”
- “Detect brute force attacks”

Use LangChain to chain agents for end-to-end responses.

---

## 📤 Output Examples

- LLM-generated timeline
- JSON summaries
- Session anomalies
- Risk scores per IP/user

---

## 🧠 Advanced Capabilities

- Vector search for log similarity (FAISS, ChromaDB)
- Named Entity Recognition
- Attack pattern detection (MITRE ATT&CK mapping)
- Auto-triage suggestions (e.g., escalate, ignore, log)

---

## 🧰 Tools Integrated

- LLMs: OpenAI, Azure OpenAI, Ollama
- Infra: Pandas, DuckDB, LangChain
- UI: Streamlit / Gradio
- Vector DBs: FAISS, Weaviate

---

## 🚨 Use Case: Lateral Movement Detection

- **Ingestor Agent** gathers endpoint & auth logs
- **Parser Agent** structures session trails
- **Analyzer Agent** finds suspicious user hops across servers
- **Insight Agent** builds timeline & MITRE ATT&CK overlay
- **UX Agent** presents findings & action options

---

## ✅ Next Steps

Would you like code scaffolding for:

- Agent controller logic?
- A Streamlit chat interface?
- Adding memory or self-healing behaviors?

