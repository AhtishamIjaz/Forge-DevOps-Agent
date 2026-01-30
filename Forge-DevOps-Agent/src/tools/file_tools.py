import subprocess
import os
from langchain_core.tools import tool

WORKSPACE_DIR = os.path.join(os.getcwd(), "workspace")
if not os.path.exists(WORKSPACE_DIR):
    os.makedirs(WORKSPACE_DIR)

@tool
def write_python_file(filename: str, code: str) -> str:
    """Writes Python code to a file in the workspace."""
    # Clean up any potential markdown accidents from the LLM
    clean_code = code.replace("```python", "").replace("```", "").strip()
    
    file_path = os.path.join(WORKSPACE_DIR, filename)
    try:
        with open(file_path, "w") as f:
            f.write(clean_code)
        return f"Successfully saved {filename}"
    except Exception as e:
        return f"Error saving file: {str(e)}"

@tool
def execute_python_code(filename: str) -> str:
    """Runs pytest on the specified file and returns the results."""
    file_path = os.path.join(WORKSPACE_DIR, filename)
    
    if not os.path.exists(file_path):
        return f"Error: File {filename} not found."

    try:
        # We now run 'pytest' instead of 'python' to get professional test reports
        result = subprocess.run(
            ["pytest", "--tb=short", file_path], 
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return f"TESTS PASSED!\n{result.stdout}"
        else:
            return f"TESTS FAILED!\n{result.stdout}\n{result.stderr}"
            
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"