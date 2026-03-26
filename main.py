import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Gemini 2.0 Flash
# Use the exact string from your terminal output
model = genai.GenerativeModel('gemini-2.0-flash')

def load_all_data():
    """Loads JSON and Markdown data from the directory."""
    data_path = 'data/'
    
    with open(os.path.join(data_path, 'tickets.json')) as f:
        tickets = json.load(f)
    with open(os.path.join(data_path, 'accounts.json')) as f:
        accounts = json.load(f)
        
    # Load knowledge base documents 
    kb_content = ""
    for filename in ['refund_policy.md', 'account_upgrade.md', 'api_rate_limits.md', 'security_practices.md', 'integration_setup.md']:
        with open(os.path.join(data_path, filename)) as f:
            kb_content += f"\n--- Source: {filename} ---\n{f.read()}\n"
            
    return tickets, accounts, kb_content

TICKETS, ACCOUNTS, KB_CONTEXT = load_all_data()

def get_triage_ranking():
    """Calculates priority scores for all open tickets [cite: 97-105]."""
    triage_results = []
    for ticket in TICKETS:
        if ticket['status'] == 'resolved':
            continue
            
        score = 0
        # Priority Weighting [cite: 100]
        p_map = {"urgent": 10, "high": 7, "medium": 4, "low": 1}
        score += p_map.get(ticket['priority'], 0)
        
        # Customer Tier Weighting [cite: 101]
        t_map = {"enterprise": 5, "pro": 3, "basic": 1}
        score += t_map.get(ticket['customer_tier'], 0)
        
        # Account Health Impact [cite: 103]
        account = next((a for a in ACCOUNTS if a['customer_name'] == ticket['customer_name']), None)
        if account and account['health_score'] < 50:
            score += 5
            
        triage_results.append({
            "ticket_id": ticket['ticket_id'],
            "customer": ticket['customer_name'],
            "score": score,
            "reason": f"Priority: {ticket['priority']}, Tier: {ticket['customer_tier']}, Health Score: {account['health_score'] if account else 'N/A'}"
        })
    
    # Sort by highest score first [cite: 99]
    ranked = sorted(triage_results, key=lambda x: x['score'], reverse=True)
    return ranked[:3]

def run_assistant(query):
    """Main routing and response engine [cite: 53-60]."""
    
    # Calculate triage data in case the route is TRIAGE
    triage_data = get_triage_ranking()
    
    system_prompt = f"""
    You are a Support Triage Assistant. Analyze the query and provide a structured response.
    
    VALID ROUTES:
    1. KNOWLEDGE_BASE: For policy or setup questions. 
    2. TICKET_LOOKUP: For specific ticket status or assigned agent. 
    3. ACCOUNT_LOOKUP: For customer plan or renewal dates. 
    4. AMBIGUOUS: Use if the query is too vague (e.g., "check that ticket"). 
    5. UNSUPPORTED: For info not in our data (e.g., HIPAA, GDPR, physical address). [cite: 57, 93]

    DATA CONTEXT:
    - Tickets: {json.dumps(TICKETS)}
    - Accounts: {json.dumps(ACCOUNTS)}
    - KB: {KB_CONTEXT}
    - Triage Ranking: {json.dumps(triage_data)}

    OUTPUT RULES:
    - Return ONLY valid JSON.
    - If route is KNOWLEDGE_BASE, cite the specific .md file. [cite: 65]
    - If route is AMBIGUOUS, ask a clarifying question. [cite: 82]
    - If query asks "what to handle first", explain the triage ranking logic. [cite: 105]
    """

    response = model.generate_content(
        f"{system_prompt}\n\nUser Query: {query}",
        generation_config={"response_mime_type": "application/json"}
    )
    
    return json.loads(response.text)

if __name__ == "__main__":
    print("--- Support Triage AI Active ---")
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ['exit', 'quit']:
            break
            
        try:
            result = run_assistant(user_input)
            print("\nStructured Decision Output:")
            print(json.dumps(result, indent=2))
        except Exception as e:
            print(f"Error: {e}")