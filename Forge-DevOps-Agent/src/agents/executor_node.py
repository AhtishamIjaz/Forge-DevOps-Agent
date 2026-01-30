from src.state.project_state import ProjectState
from src.tools.file_tools import write_python_file, execute_python_code

def executor_node(state: ProjectState):
    """
    The Executor: Saves files to disk and runs the tests.
    """
    print(f"--- EXECUTOR: RUNNING TESTS ON DISK ---")
    
    # 1. Save the main code
    for filename, code in state["code_samples"].items():
        write_python_file.invoke({"filename": filename, "code": code})
        
    # 2. Save the test code
    for filename, test_code in state["tests"].items():
        write_python_file.invoke({"filename": filename, "code": test_code})
    
    # 3. Execute the tests using pytest
    # We run 'pytest' as a shell command through our tool
    # Note: On some systems you might need to run 'python -m pytest'
    execution_result = execute_python_code.invoke({"filename": "test_main.py"})
    
    errors = []
    is_finished = False
    
    if "Failed" in execution_result or "Error" in execution_result:
        errors.append(execution_result)
        status = "Tests failed. Sending back to Coder."
    else:
        is_finished = True
        status = "Tests passed! Software is finalized."

    return {
        "errors": errors,
        "is_finished": is_finished,
        "current_status": status
    }