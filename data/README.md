# AI-Powered Support Triage Assistant

An agentic AI system designed to classify, retrieve, and prioritize customer support requests for a SaaS platform.

## Setup Instructions
1. Clone this repository.
2. Create a virtual environment: `python -m venv venv && source venv/bin/activate`.
3. Install dependencies: `pip install google-generativeai python-dotenv`.
4. Create a `.env` file based on `.env.example` and add your `GEMINI_API_KEY`.

## Running the System
Run the main script:
```bash
python main.py