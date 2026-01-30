import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from src.state.project_state import ProjectState
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant", # Using the smaller, faster model for simple test generation
    temperature=0.1,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

def tester_node(state: ProjectState):
    """
    The Tester Agent: Generates unit tests for the provided code.
    """
    print(f"--- TESTER AGENT: GENERATING TESTS ---")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are a Quality Assurance Engineer. Your job is to write professional Python unit tests "
            "using the 'pytest' framework. \n\n"
            "Rules:\n"
            "1. Only return the test code. No explanations, no markdown backticks.\n"
            "2. Ensure you test edge cases (empty inputs, wrong types, etc.).\n"
            "3. Assume the file to test is named 'main.py'."
        )),
        ("human", "Code to test:\n\n{code_samples}")
    ])

    chain = prompt | llm
    
    # We pass the code from main.py to the tester
    code_to_test = state["code_samples"].get("main.py", "")
    response = chain.invoke({"code_samples": code_to_test})

    return {
        "tests": {"test_main.py": response.content},
        "current_status": "Tests generated. Moving to execution."
    }