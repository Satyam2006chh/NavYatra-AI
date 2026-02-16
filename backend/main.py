"""
FastAPI Backend — NavYatra AI
Exposes the travel planning graph as a REST API.
"""

import os
import sys

# Ensure project root is in path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from dotenv import load_dotenv

# Load .env from project root explicitly
ENV_PATH = os.path.join(PROJECT_ROOT, ".env")
load_dotenv(dotenv_path=ENV_PATH, override=True)

print(f"📂 Loading .env from: {ENV_PATH}")
print(f"🔑 CEREBRAS_API_KEY present: {'YES' if os.getenv('CEREBRAS_API_KEY') else 'NO - MISSING!'}")

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from graph.workflow import run_travel_plan

app = FastAPI(
    title="NavYatra AI",
    description="Multi-Agent Travel Intelligence & Planning System",
    version="1.0.0"
)

# Allow Streamlit to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PlanRequest(BaseModel):
    query: str
    thread_id: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    service: str


@app.get("/api/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy", service="NavYatra AI")


@app.post("/api/plan")
def create_travel_plan(request: PlanRequest):
    """
    Generate a complete travel plan from a natural language query.

    The query goes through the multi-agent graph:
    Coordinator → [Flight + Hotel + Weather + Research] (parallel) → Itinerary Agent
    """
    # Re-load env to pick up any changes
    load_dotenv(dotenv_path=ENV_PATH, override=True)

    cerebras_key = os.getenv("CEREBRAS_API_KEY", "")
    if not cerebras_key:
        raise HTTPException(
            status_code=500,
            detail="CEREBRAS_API_KEY is missing! Please add your Cerebras API key to the .env file and save it (Ctrl+S)."
        )

    try:
        result = run_travel_plan(
            user_query=request.query,
            thread_id=request.thread_id
        )
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
