# GEN-AI

Practical GenAI learning workspace with multiple mini-projects covering prompting, embeddings, agents, RAG, LangGraph, human-in-the-loop workflows, and queue-based processing.

## Project Modules

- `01-tokenization` - Tokenization basics examples.
- `02-vector-embedding` - Embedding generation basics.
- `03-hello-world` - Intro chat completion and prompting scripts.
- `04-agent` - Agent workflow examples + simple todo frontend.
- `05-rag-1` - Basic RAG flow with sample document.
- `06_langgraph` - LangGraph starter scripts.
- `08_tool` - Tool-enabled graph examples.
- `09_human_in_loop` - Human-in-the-loop graph examples.
- `chat_graph` - Additional conversational graph experiments.
- `memory` - Memory-focused experiments.
- `rag_queue` - Queue-based RAG processing structure.
- `policy_bot` - Policy ingestion/server/worker workflow.
- `vibe_talk` - App and chat UI experiments.
- `lanngfuse` - Docker compose setup for observability/local infra.

## Quick Setup

1. Clone the repository.
2. Create and activate Python virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Add environment variables in `.env` (example: API keys).
5. Run scripts from the specific module directory.

## Notes

- Large/local-only folders like `venv/` and `node_modules/` are ignored.
- Keep secrets in `.env`, never hardcode keys in source files.
