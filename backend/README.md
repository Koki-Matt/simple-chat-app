# Simple Chat Backend (FastAPI)

## Quickstart

```bash
cd /Users/kokimatsushita/Codes/simple-chat-app
python3 -m venv backend/.venv
source backend/.venv/bin/activate
pip install --upgrade pip
pip install "fastapi" "uvicorn[standard]" "pydantic-settings"
# Optional heavy packages (only if you need them):
# pip install "transformers" "torch"

# Save dependencies
pip freeze > backend/requirements.txt

# Run the server
uvicorn app.main:app --app-dir backend --reload --host 0.0.0.0 --port 8000

# Run the Gradio UI (in another terminal)
python backend/gradio_ui.py
```

## Endpoints

- Health: `GET /api/v1/health`
- List messages: `GET /api/v1/messages`
- Create message: `POST /api/v1/messages` with body `{ "text": "hello" }`
- Generate text: `POST /api/v1/generate` with body `{ "prompt": "Hello world", "max_length": 50, "temperature": 0.7 }`

## Test with curl

```bash
curl http://localhost:8000/api/v1/health
curl http://localhost:8000/api/v1/messages
curl -X POST http://localhost:8000/api/v1/messages \
  -H "Content-Type: application/json" \
  -d '{"text":"hello"}'
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"The future of AI is","max_length":30,"temperature":0.8}'
```

## Gradio Web UI

The app includes a Gradio web interface for easy interaction:

### Important: Virtual Environment Required for Both Terminals

Both the FastAPI server and Gradio UI need access to the same Python packages, so you must activate the virtual environment in **both terminals**.

1. **Start the API server** (Terminal 1):

   ```bash
   cd /Users/kokimatsushita/Codes/simple-chat-app
   source backend/.venv/bin/activate  # ← REQUIRED
   uvicorn app.main:app --app-dir backend --reload --host 0.0.0.0 --port 8000
   ```

2. **Start the Gradio UI** (Terminal 2):

   ```bash
   cd /Users/kokimatsushita/Codes/simple-chat-app
   source backend/.venv/bin/activate  # ← REQUIRED
   python backend/gradio_ui.py
   ```

3. **Open your browser** to `http://localhost:7860`

### Why Both Terminals Need Virtual Environment?

- **Terminal 1 (FastAPI)**: Needs `fastapi`, `uvicorn`, `transformers`, `torch`, `pydantic-settings`
- **Terminal 2 (Gradio)**: Needs `gradio`, `requests` to call the API

Without the virtual environment, you'll get `ModuleNotFoundError` in both terminals.

### UI Features:

- ✅ API status checker
- 🎛️ Interactive parameter controls (max_length, temperature)
- 📝 Example prompts
- 🔄 Real-time text generation
- 📱 Responsive design
