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
