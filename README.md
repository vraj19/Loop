# Loop 
Loop is a personal intelligence runtime that combines persistent memory, knowledge graphs, and semantic retrieval to power personal agents

The idea is simple: agents need memory, Loop provides a runtime that captures events from a user's digital life, stores them locally, and allows agents to reason over that memory.

Loop combines:
- persistent memory
- semantic retrieval
- knowledge graphs
- an agent runtime

The goal is to build agents that understand context across time instead of operating on isolated prompts.

## Architecture

Loop is built around a memory‑first architecture.

```
Sources (files, browser, messaging)
        ↓
Event ingestion
        ↓
Loop Core (memory + embeddings + graph)
        ↓
Agent runtime
        ↓
Applications
```

Loop captures events from a user's digital life, stores them locally, and makes them retrievable through semantic search and structured relationships.

Agents then use this memory to reason, plan, and act with long‑term context.

---

## Installation

### Using Conda (Recommended for Apple Silicon/macOS)

1. Install [Miniforge](https://github.com/conda-forge/miniforge#miniforge3) if you don't have conda.
2. Create the environment:
   ```sh
   conda env create -f environment.yml
   conda activate loop-env
   ```

### Using pip (Open Source Friendly)

1. Create a virtual environment named `loop-env`:
   ```sh
   python3 -m venv loop-env
   source loop-env/bin/activate
   pip install -r requirements.txt
   ```

---

## Notes
- For best compatibility on Apple Silicon, use the conda environment.
- If you use pip, some ML packages may require additional system dependencies or may not be as optimized.
- After setup, run your scripts as usual inside the activated environment.