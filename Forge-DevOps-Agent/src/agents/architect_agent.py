import os
from langchain_groq import ChatGroq
from src.state.project_state import ProjectState
from dotenv import load_dotenv

load_dotenv()

# Logic Base: Initializing the Groq engine specifically
# We use llama-3.3-70b because it is excellent at technical planning
llm = ChatGroq(
    temperature=0,
    model_name="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY")
)

def architect_node(state: ProjectState):
    print("--- ARCHITECT: DESIGNING SOLUTION ---")
    
    prompt = f"""
    You are an Expert Software Architect. Analyze this user requirement:
    "{state['requirement']}"

    1. Identify the Scenario: (e.g., Data Science, Web Scraper, CLI Tool, Math Predictor).
    2. Define Logic/Formulas: (e.g., If BMI, use weight / height squared).
    3. List Dependencies: (Which libraries are needed?).
    4. Step-by-Step Plan: Create a technical roadmap for the Coder.

    Output ONLY the technical plan.
    """
    
    response = llm.invoke(prompt)
    
    return {
        "plan": response.content,
        "current_status": "Architect has finalized the plan. Moving to Coding."
    }