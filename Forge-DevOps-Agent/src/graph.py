import sqlite3
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver

from src.state.project_state import ProjectState
from src.agents.architect_agent import architect_node # NEW AGENT
from src.agents.coder_agent import coder_node
from src.agents.tester_agent import tester_node
from src.agents.executor_node import executor_node

# --- ROUTER LOGIC ---
def should_continue(state: ProjectState):
    if state["is_finished"]:
        return END
    if state["iteration_count"] >= 10: # Increased for robustness
        return END
    return "coder"

# --- GRAPH SETUP ---
workflow = StateGraph(ProjectState)

workflow.add_node("architect", architect_node)
workflow.add_node("coder", coder_node)
workflow.add_node("tester", tester_node)
workflow.add_node("executor", executor_node)

# Flow: Start -> Plan -> Code -> Test -> Execute -> (Loop)
workflow.add_edge(START, "architect")
workflow.add_edge("architect", "coder")
workflow.add_edge("coder", "tester")
workflow.add_edge("tester", "executor")

workflow.add_conditional_edges(
    "executor",
    should_continue,
    {"coder": "coder", END: END}
)

# Persistence
conn = sqlite3.connect("agent_memory.db", check_same_thread=False)
memory = SqliteSaver(conn)
app = workflow.compile(checkpointer=memory)