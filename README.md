
# Model to Agent (Gemini + LangChain)

This repo is a small, progressive set of Python scripts that show the path from:

1. **A basic LLM chatbot**
2. **A chatbot with conversation memory**
3. **A “tool-using” assistant** (simple routing + Tavily web search)

The examples use **Google Gemini** via `langchain-google-genai`.

## What’s inside

- `basic_chatbot.py` — minimal loop: prompt → model → response
- `memory_chatbot.py` — keeps a `chat_history` list (messages) and sends it each turn
- `agent_tools.py` — adds a tiny decision layer to call **Tavily** web search for “current events” style queries

## Requirements

- Python **3.10+** (3.11 recommended)
- A **Google AI / Gemini API key**
- (Optional) A **Tavily API key** for `agent_tools.py`

## Setup (Windows / PowerShell)

1) Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Install dependencies:

```powershell
pip install -r requirements.txt
```

3) Create a `.env` file in the project root:

```dotenv
GOOGLE_API_KEY=your_google_api_key_here

# Only needed for agent_tools.py
TAVILY_API_KEY=your_tavily_api_key_here
```

Tip: there is an `.env.example` you can copy.

## Run

Basic chatbot:

```powershell
python basic_chatbot.py
```

Chatbot with memory:

```powershell
python memory_chatbot.py
```

Tool-using assistant (memory + web search):

```powershell
python agent_tools.py
```

## Environment variables

- `GOOGLE_API_KEY` (required) — Gemini API key
- `TAVILY_API_KEY` (optional) — required only if you run `agent_tools.py`

## Notes

- These scripts are intentionally simple and run in an infinite loop; press `Ctrl+C` to exit.
- Avoid committing secrets: **never** commit `.env` to GitHub.

## License

See [LICENSE](LICENSE) (CC BY-NC 4.0).

