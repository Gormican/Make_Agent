\# Chuckie MCP Server



FastAPI MCP-style HTTP service for Make.com agents.



\## Endpoints



\- `GET /mcp/v1/health` — public liveness.

\- `GET /mcp/v1/context` — \*\*Bearer\*\*; starter context.

\- `POST /mcp/v1/morning-report` — \*\*Bearer\*\*; returns short, speakable lines.

\- `POST /mcp/v1/reminder` — \*\*Bearer\*\*; stub scheduler.

\- `POST /mcp/v1/quiz/next` — \*\*Bearer\*\*; quiz stub.



Swagger: `/mcp/v1/docs`  

OpenAPI: `/mcp/v1/openapi.json`



\## Run locally



```bash

python -m venv .venv

\# Windows PowerShell:

.\\.venv\\Scripts\\Activate.ps1

pip install -r requirements.txt



\# set an API key for the padlock

$env:API\_KEY="super-secret-key"



\# start

uvicorn mcp\_server:app --reload

\# http://127.0.0.1:8000/mcp/v1/health



