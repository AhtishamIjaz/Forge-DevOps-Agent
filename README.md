cat <<EOF > README.md
# 🛠️ Forge-DevOps-Agent

An AI-powered DevOps assistant designed to automate infrastructure tasks, code generation, and testing using advanced LLM orchestration.

## 🚀 Features
* **Architect Agent:** Designs system structures.
* **Coder Agent:** Generates Python-based solutions.
* **Tester Agent:** Ensures code quality and reliability.
* **Memory Management:** Uses SQLite to maintain project state and logs.

## 🛠️ Tech Stack
* **Language:** Python 3.11+
* **LLM Orchestration:** LangChain / LangGraph
* **Inference:** Groq Cloud API
* **Database:** SQLite (agent_memory.db)

## 📦 Installation & Setup
1. Clone the repository:
   \`\`\`bash
   git clone https://github.com/AhtishamIjaz/Forge-DevOps-Agent.git
   \`\`\`
2. Install dependencies:
   \`\`\`bash
   pip install -r Forge-DevOps-Agent/requirements.txt
   \`\`\`
3. Configure your environment:
   * Create a \`.env\` file in the root directory.
   * Add your \`GROQ_API_KEY\` and \`LANGCHAIN_API_KEY\`.

## 🛡️ License
Distributed under the MIT License.
EOF
