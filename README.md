

# Adversarial-Edge-Case-Discovery-Agent-for-Autonomous-Vehicles


[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI GPT-4o](https://img.shields.io/badge/AI-GPT--4o-orange.svg)](https://openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---
## 🔬 Project Overview
In autonomous driving, the "Safety Envelope" is defined by rare, high-risk scenarios that traditional testing often misses. This system addresses two critical challenges in modern AV validation:
1. **Agentic Boundary Discovery:** Transitioning from manual scenario creation to an **Agentic Search** where the AI actively seeks to "break" the AV controller.
2. **Qualitative Safety Auditing:** Implementing an **LLM-as-a-Judge** architecture to provide semantic reasoning for failures, rather than relying on raw distance metrics alone.
---
## 🚀 Key Capabilities
* **Multi-Agent Orchestration:** Utilizes a dual-agent architecture—a **Scenario Planner** (Adversarial) and an **LLM-as-a-Judge** (Evaluator).
* **Closed-Loop Adversarial Search:** Achieved a **40% Attack Success Rate (ASR)**, autonomously reducing Time-to-Collision (TTC) from 2.5s to 0.1s.
* **Proactive Risk Evaluation:** The Judge Agent audits every simulation run, providing a reasoning feedback signal to the Planner for iterative optimization.
* **Standardized Artifact Generation:** Automatically exports critical edge cases into **ASAM OpenSCENARIO (.xosc)** format for high-fidelity simulation injection.
---
## 🛠️ Tech Stack
| Category | Tools |
| :--- | :--- |
| **Agentic Framework** | OpenAI GPT-4o, LLM-as-a-Judge |
| **Data & Logic** | Python 3.10+, Pydantic (Strict Schema), NumPy |
| **Standards** | ASAM OpenSCENARIO (XML Schema) |
| **Infrastructure** | GitHub Actions, Python-dotenv, Logging/Telemetry |
| **Simulation** | Deterministic SiL Physics Engine |
---
## 📂 Project Structure
```text
├── src/
│   ├── agents/           # Agentic logic (Scenario Planner & LLM Judge)
│   ├── simulation/       # SiL Engine (Deterministic physics & TTC calculation)
│   ├── pipeline/         # Execution scripts for the adversarial loop
│   ├── entity/           # Pydantic schemas for scenario parameters
│   ├── config.py         # Global settings and API configurations
│   └── utils/            # Helper functions for XML templating and logging
├── data/
│   ├── templates/        # .xosc base templates for cut-in maneuvers
│   └── results/          # Auto-generated edge case artifacts (.xosc)
├── Artifacts/            # Serialized models and experiment drift reports
├── main.py               # Entry point for the discovery loop
└── .env                  # API Key storage (Ignored by git)

```
---
## 🔄 Adversarial Workflow

1. **Memory & History:** Retrieve the outcome of previous runs (TTC, speeds, lateral offsets).
2. **Planner Reasoning:** GPT-4o analyzes failures and hallucinates new, riskier parameters to exploit the AV's braking logic.
3. **SiL Execution:** The Physics Engine runs the maneuver and calculates the **Time-To-Collision (TTC)**.
4. **Safety Audit:** The **Judge Agent** evaluates the "criticality" and provides a natural language feedback signal to guide the next iteration.
---
## 🚀 Getting Started

### 1. Installation

```bash
git clone [https://github.com/Gauti555/Adversarial-Edge-Case-Discovery-Agent-for-Autonomous-Vehicles.git](https://github.com/Gauti555/Adversarial-Edge-Case-Discovery-Agent-for-Autonomous-Vehicles.git)
cd Adversarial-Edge-Case-Discovery-Agent-for-Autonomous-Vehicles
pip install -r requirements.txt

```

### 2. Configure Environment

Create a `.env` file or export your key:

```bash
export OPENAI_API_KEY='sk-your-key-here'

```

### 3. Run the Discovery Agent

```bash
python -m src.main

```

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

```

