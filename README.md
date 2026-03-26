# AI-Powered Support Triage Assistant

An intelligent reasoning engine built for a SaaS support environment. [cite_start]This system classifies incoming queries and decides whether to retrieve information from a knowledge base, query structured databases, or request more information—all while providing a structured decision object for every response [cite: 36-46].

## 📂 Project Overview
[cite_start]This assistant implements an automated triage pipeline with the following capabilities [cite: 53-105]:
* [cite_start]**Query Routing:** Categorizes requests into 5 distinct routes: `KNOWLEDGE_BASE`, `TICKET_LOOKUP`, `ACCOUNT_LOOKUP`, `AMBIGUOUS`, or `UNSUPPORTED` [cite: 54-57].
* [cite_start]**Knowledge Base Retrieval (RAG):** Uses documentation to answer informational queries and cites the specific source files [cite: 61-66].
* [cite_start]**Structured Data Lookup:** Filters `tickets.json` and `accounts.json` to answer specific status and account health queries [cite: 67-80].
* [cite_start]**Weighted Triage Ranking:** A custom algorithm that prioritizes issues by combining ticket priority, customer tier (Enterprise vs. Basic), and account health scores [cite: 97-105].
* [cite_start]**Hallucination Prevention:** Explicitly refuses queries that fall outside the provided data scope [cite: 90-96].

## 🛠️ Setup & Installation
[cite_start]Ensure you have **Python 3.10+** and **pip** installed on your machine [cite: 19-21].

### 1. Environment Setup
```bash
# Clone the repository
git clone [https://github.com/laraibgul1119/AI_Powered_Triage_AI_Assistant.git](https://github.com/laraibgul1119/AI_Powered_Triage_AI_Assistant.git)
cd AI_Powered_Triage_AI_Assistant

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
