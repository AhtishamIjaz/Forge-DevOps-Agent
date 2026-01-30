import streamlit as st
from src.graph import app

st.set_page_config(page_title="Universal Forge Agent", layout="wide")
st.title("🚀 Universal DevOps Agent")

with st.sidebar:
    thread_id = st.text_input("Project ID", value="universal_test_01")

user_input = st.text_area("What should I build?")

if st.button("Start Build"):
    inputs = {"requirement": user_input, "iteration_count": 0, "is_finished": False}
    config = {"configurable": {"thread_id": thread_id}}
    
    # Columns for UI
    col_plan, col_code = st.columns(2)
    
    for event in app.stream(inputs, config=config):
        for node, values in event.items():
            st.write(f"**Current Phase:** {node}")
            
            if "plan" in values:
                with col_plan:
                    st.info("### 📋 Architect's Plan")
                    st.write(values["plan"])
            
            if "code_samples" in values:
                with col_code:
                    st.success("### 💻 Current Code")
                    st.code(values["code_samples"].get("main.py", ""))

            if values.get("is_finished"):
                st.balloons()
                st.success("Software Complete!")