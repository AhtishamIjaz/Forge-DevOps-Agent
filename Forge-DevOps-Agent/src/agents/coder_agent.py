import re
import os
from langchain_groq import ChatGroq
from src.state.project_state import ProjectState
from dotenv import load_dotenv

load_dotenv()

# Logic Base: Reusing the Groq engine for fast code generation
llm = ChatGroq(
    temperature=0,
    model_name="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY")
)

def coder_node(state: ProjectState):
    iteration = state.get("iteration_count", 0) + 1
    print(f"--- CODER: ATTEMPT {iteration} ---")
    
    prompt = f"""
    You are a Senior Python Developer. 
    
    ARCHITECT'S PLAN: 
    {state['plan']}
    
    USER REQUIREMENT: 
    {state['requirement']}
    
    PAST ERRORS (If any):
    {state.get('errors', 'No errors.')}

    STRICT RULES:
    1. Follow the Architect's Plan exactly.
    2. Use the mathematical formulas provided in the plan.
    3. Provide ONLY the code for 'main.py' inside triple backticks (```python ... ```).
    4. Ensure no conversational text is included.
    """
    
    response = llm.invoke(prompt)
    content = response.content

    # Logic Base: Regex extraction to clean AI chat around the code
    code_match = re.search(r"```python\n(.*?)\n```", content, re.DOTALL)
    if not code_match:
        code_match = re.search(r"```(.*?)\n```", content, re.DOTALL)
        
    clean_code = code_match.group(1) if code_match else content

    return {
        "code_samples": {"main.py": clean_code},
        "current_status": f"Code generated (Attempt {iteration}). Sending to Tester.",
        "iteration_count": iteration
    }