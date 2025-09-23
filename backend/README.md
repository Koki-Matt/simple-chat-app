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

## Test with curl

```bash
curl http://localhost:8000/api/v1/health
curl http://localhost:8000/api/v1/messages
curl -X POST http://localhost:8000/api/v1/messages \
  -H "Content-Type: application/json" \
  -d '{"text":"hello"}'
```
