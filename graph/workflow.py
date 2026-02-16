"""
LangGraph Workflow — NavYatra AI
Defines the multi-agent graph with parallel execution and SQLite checkpointer.

Graph Flow:
  START → coordinator → [flight, hotel, weather, research] (parallel) → itinerary → END
"""

import os
import sys
import sqlite3
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langgraph.graph import StateGraph, START, END
from graph.state import TravelPlanState
from agents.coordinator import parse_user_query
from agents.flight_agent import run_flight_agent
from agents.hotel_agent import run_hotel_agent
from agents.weather_agent import run_weather_agent
from agents.research_agent import run_research_agent
from agents.itinerary_agent import generate_itinerary

# Checkpointer setup
try:
    from langgraph.checkpoint.sqlite import SqliteSaver
    DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "navyatra.db")
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    checkpointer = SqliteSaver(conn)
    print("✅ Using SQLite checkpointer for persistence")
except ImportError:
    from langgraph.checkpoint.memory import MemorySaver
    checkpointer = MemorySaver()
    print("⚠️ Using MemorySaver (install langgraph-checkpoint-sqlite for persistence)")


# ============================================================
# GRAPH NODES — No delays! Cerebras has 1M TPD.
# ============================================================

def coordinator_node(state: TravelPlanState) -> dict:
    """Node 1: Parse user query into structured travel data."""
    print("\n🎯 [Coordinator] Parsing user query...")
    parsed = parse_user_query(state["user_query"])
    print(f"✅ [Coordinator] Parsed: {parsed}")
    return {"parsed_input": parsed}


def flight_node(state: TravelPlanState) -> dict:
    """Node 2: Search and analyze flights (runs in parallel)."""
    print("✈️  [Flight Agent] Searching flights...")
    p = state["parsed_input"]

    result = run_flight_agent(
        f"Search flights from {p['origin_city']} to {p['destination_city']} "
        f"on {p['departure_date']} for {p['adults']} adult(s) in {p['currency']}."
    )

    print("✅ [Flight Agent] Done")
    return {"flight_results": result}


def hotel_node(state: TravelPlanState) -> dict:
    """Node 3: Search and analyze hotels (runs in parallel)."""
    print("🏨 [Hotel Agent] Searching hotels...")
    p = state["parsed_input"]

    input_text = (
        f"Find hotels in {p['destination_city']}. "
        f"The traveler is coming from {p['origin_city']} for {p.get('num_days', 3)} days."
    )
    if p.get("preferences"):
        input_text += f" Preferences: {p['preferences']}"

    result = run_hotel_agent(input_text)
    print("✅ [Hotel Agent] Done")
    return {"hotel_results": result}


def weather_node(state: TravelPlanState) -> dict:
    """Node 4: Analyze weather conditions (runs in parallel)."""
    print("🌤️  [Weather Agent] Checking weather...")
    p = state["parsed_input"]

    result = run_weather_agent(
        f"Check the weather in {p['destination_city']} for a trip "
        f"starting {p['departure_date']} for {p.get('num_days', 3)} days."
    )

    print("✅ [Weather Agent] Done")
    return {"weather_results": result}


def research_node(state: TravelPlanState) -> dict:
    """Node 5: Research attractions and local tips (runs in parallel)."""
    print("🎯 [Research Agent] Researching destination...")
    p = state["parsed_input"]

    input_text = (
        f"Research the best tourist attractions, food, culture, and travel tips "
        f"for {p['destination_city']}."
    )
    if p.get("preferences"):
        input_text += f" The traveler is interested in: {p['preferences']}"

    result = run_research_agent(input_text)
    print("✅ [Research Agent] Done")
    return {"research_results": result}


def itinerary_node(state: TravelPlanState) -> dict:
    """Node 6: Synthesize everything into a final travel plan."""
    print("📋 [Itinerary Agent] Generating final travel plan...")
    p = state["parsed_input"]

    itinerary = generate_itinerary(
        flight_results=state.get("flight_results", "No flight data available"),
        hotel_results=state.get("hotel_results", "No hotel data available"),
        weather_results=state.get("weather_results", "No weather data available"),
        research_results=state.get("research_results", "No research data available"),
        num_days=p.get("num_days", 3)
    )

    print("✅ [Itinerary Agent] Final plan generated!")
    return {"itinerary": itinerary}


# ============================================================
# BUILD THE GRAPH — Parallel fan-out for 4 middle agents
# ============================================================

def build_graph():
    """Build and compile the LangGraph workflow with parallel execution."""
    builder = StateGraph(TravelPlanState)

    builder.add_node("coordinator", coordinator_node)
    builder.add_node("flight_agent", flight_node)
    builder.add_node("hotel_agent", hotel_node)
    builder.add_node("weather_agent", weather_node)
    builder.add_node("research_agent", research_node)
    builder.add_node("itinerary_agent", itinerary_node)

    # Coordinator runs first
    builder.add_edge(START, "coordinator")

    # Fan-out: coordinator → all 4 agents run in PARALLEL
    builder.add_edge("coordinator", "flight_agent")
    builder.add_edge("coordinator", "hotel_agent")
    builder.add_edge("coordinator", "weather_agent")
    builder.add_edge("coordinator", "research_agent")

    # Fan-in: all 4 agents → itinerary (waits for all to complete)
    builder.add_edge("flight_agent", "itinerary_agent")
    builder.add_edge("hotel_agent", "itinerary_agent")
    builder.add_edge("weather_agent", "itinerary_agent")
    builder.add_edge("research_agent", "itinerary_agent")

    builder.add_edge("itinerary_agent", END)

    graph = builder.compile(checkpointer=checkpointer)
    return graph


# ============================================================
# RUN THE GRAPH
# ============================================================

def run_travel_plan(user_query: str, thread_id: str = None) -> dict:
    """Execute the full travel planning workflow."""
    graph = build_graph()

    if not thread_id:
        thread_id = str(uuid.uuid4())

    config = {"configurable": {"thread_id": thread_id}}

    initial_state = {
        "user_query": user_query,
        "parsed_input": {},
        "flight_results": "",
        "hotel_results": "",
        "weather_results": "",
        "research_results": "",
        "itinerary": ""
    }

    print(f"\n{'='*60}")
    print(f"🧭 NAVYATRA AI — Starting Travel Plan (Parallel Mode)")
    print(f"📝 Query: {user_query}")
    print(f"🧵 Thread: {thread_id}")
    print(f"{'='*60}\n")

    result = graph.invoke(initial_state, config=config)

    return {
        "thread_id": thread_id,
        "parsed_input": result.get("parsed_input", {}),
        "flight_results": result.get("flight_results", ""),
        "hotel_results": result.get("hotel_results", ""),
        "weather_results": result.get("weather_results", ""),
        "research_results": result.get("research_results", ""),
        "itinerary": result.get("itinerary", "")
    }
