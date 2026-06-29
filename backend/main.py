"""
is FastAPI Backend — NavYatra AI
Exposes the travel planning graph as a REST API.
"""

import os
import sys

# Ensure project root is in path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

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
    # User-provided API keys
    cerebras_api_key: Optional[str] = None
    serpapi_key: Optional[str] = None
    rapidapi_key: Optional[str] = None
    openweather_api_key: Optional[str] = None


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

    API keys are provided by the user via the frontend UI.
    """
    # Set user-provided API keys as environment variables
    # so existing API clients (os.getenv) pick them up automatically
    key_mapping = {
        "CEREBRAS_API_KEY": request.cerebras_api_key,
        "SERPAPI_KEY": request.serpapi_key,
        "RAPIDAPI_KEY": request.rapidapi_key,
        "OPENWEATHER_API_KEY": request.openweather_api_key,
    }

    for env_name, value in key_mapping.items():
        if value:
            os.environ[env_name] = value

    try:
        result = run_travel_plan(
            user_query=request.query,
            thread_id=request.thread_id
        )
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


from fastapi.responses import StreamingResponse
import json

@app.post("/api/plan_stream")
def stream_travel_plan_endpoint(request: PlanRequest):
    """
    Stream the travel plan execution progress as Server-Sent Events (SSE).
    Yields live updates as each agent completes.
    """
    key_mapping = {
        "CEREBRAS_API_KEY": request.cerebras_api_key,
        "SERPAPI_KEY": request.serpapi_key,
        "RAPIDAPI_KEY": request.rapidapi_key,
        "OPENWEATHER_API_KEY": request.openweather_api_key,
    }
    for env_name, value in key_mapping.items():
        if value:
            os.environ[env_name] = value

    from graph.workflow import run_travel_plan_stream

    def event_generator():
        try:
            for event in run_travel_plan_stream(request.query, request.thread_id):
                yield f"data: {json.dumps(event)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
