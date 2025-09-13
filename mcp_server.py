from typing import List, Optional
from fastapi import FastAPI, Depends, Header, HTTPException, status
from pydantic import BaseModel
import os

app = FastAPI(
    title="Chuckie MCP Server",
    version="1.0.0",
    openapi_url="/mcp/v1/openapi.json",
    docs_url="/mcp/v1/docs",
    redoc_url="/mcp/v1/redoc",
)

# ---------- Auth ----------
def get_api_key(authorization: Optional[str] = Header(None)):
    """Simple Bearer token gate using API_KEY env var."""
    expected = os.getenv("API_KEY")
    if not expected:
        # If you forgot to set API_KEY on the host, leave the door shut.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Server misconfigured: API_KEY not set",
        )
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Bearer token")
    token = authorization.split(" ", 1)[1].strip()
    if token != expected:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API key")
    return True

# ---------- Models ----------
class MorningReportIn(BaseModel):
    city: str
    topics: List[str] = []
    stocks: Optional[List[str]] = None
    weekly_goal: Optional[str] = None

class MorningReportOut(BaseModel):
    lines: List[str]

class ReminderIn(BaseModel):
    text: str
    when_iso: Optional[str] = None  # ISO8601 timestamp string

class ReminderOut(BaseModel):
    id: str
    status: str = "scheduled"

class ContextOut(BaseModel):
    city: str = "Coronado"
    topics: List[str] = ["markets", "Padres", "AI"]
    weekly_goal: str = "Ship agent v1"

# Quiz
class QuizNextIn(BaseModel):
    topic: Optional[str] = None         # e.g., "biology", "algebra"
    difficulty: Optional[str] = "easy"  # "easy" | "medium" | "hard"
    num_choices: Optional[int] = 4

class QuizNextOut(BaseModel):
    id: str
    question: str
    choices: List[str]
    correct_index: int

# ---------- Public ----------
@app.get("/mcp/v1/health")
def health():
    return {"status": "OK"}

# ---------- Protected (Bearer) ----------
@app.get("/mcp/v1/context", response_model=ContextOut, dependencies=[Depends(get_api_key)])
def get_context():
    """Seed data your Make agent can fetch at the start of a scenario."""
    return ContextOut()

@app.post("/mcp/v1/morning-report", response_model=MorningReportOut, dependencies=[Depends(get_api_key)])
def morning_report(body: MorningReportIn):
    """Returns short, speakable lines your Agent can read out."""
    lines = [
        f"Good morning from {body.city}.",
    ]
    if body.topics:
        lines.append("Today’s brief: " + ", ".join(body.topics) + ".")
    if body.stocks:
        lines.append("Watching tickers: " + ", ".join(body.stocks) + ".")
    if body.weekly_goal:
        lines.append(f"This week’s goal: {body.weekly_goal}.")
    lines.append("Have a ripper day.")
    return MorningReportOut(lines=lines)

@app.post("/mcp/v1/reminder", response_model=ReminderOut, dependencies=[Depends(get_api_key)])
def create_reminder(body: ReminderIn):
    """
    Stub that pretends to schedule a reminder.
    Wire this to Make Data Store or a calendar later.
    """
    rid = "rem_" + str(abs(hash(body.text)) % 10_000_000)
    return ReminderOut(id=rid, status="scheduled")

@app.post("/mcp/v1/quiz/next", response_model=QuizNextOut, dependencies=[Depends(get_api_key)])
def quiz_next(body: QuizNextIn):
    """Tiny stub question; replace with a bank later."""
    q = "Which organelle is the powerhouse of the cell?"
    choices = ["Ribosome", "Mitochondrion", "Golgi apparatus", "Lysosome"]
    n = body.num_choices or 4
    if n < 2:
        n = 2
    return QuizNextOut(
        id="q_0001",
        question=q,
        choices=choices[:n],
        correct_index=1
    )
