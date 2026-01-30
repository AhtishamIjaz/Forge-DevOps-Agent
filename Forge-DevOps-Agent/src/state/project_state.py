from typing import TypedDict, List, Dict

class ProjectState(TypedDict):
    requirement: str
    plan: str              # NEW: The roadmap for the logic
    code_samples: Dict[str, str]
    tests: Dict[str, str]
    errors: List[str]
    iteration_count: int
    is_finished: bool
    current_status: str