
import os
import sys
import sqlite3
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langgraph.graph import StateGraph, START, END
from graph.state import TravelPlanState
from agents.coordinator import parse_user_query
from agents.itinerary_agent import generate_itinerary
from api.flights import FlightClient
from api.hotels import HotelClient
from api.weather import WeatherClient
from api.research import ResearchClient
from api.trains import TrainClient
from agents.llm_utils import get_llm, invoke_with_retry
from langchain_core.messages import SystemMessage, HumanMessage

try:
    from langgraph.checkpoint.sqlite import SqliteSaver
    DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "navyatra.db")
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    checkpointer = SqliteSaver(conn)
    print("[OK] Using SQLite checkpointer for persistence")
except ImportError:
    from langgraph.checkpoint.memory import MemorySaver
    checkpointer = MemorySaver()
    print("⚠️ Using MemorySaver (install langgraph-checkpoint-sqlite for persistence)")


# ============================================================
# ============================================================

def coordinator_node(state: TravelPlanState) -> dict:
    print("\n🎯 [Coordinator] Parsing user query...")
    parsed = parse_user_query(state["user_query"])
    print(f"✅ [Coordinator] Parsed: {parsed}")
    return {"parsed_input": parsed}


def flight_node(state: TravelPlanState) -> dict:
    p = state["parsed_input"]
    fc = FlightClient()
    raw_data = fc.search(p['origin_airport'], p['destination_airport'], p['departure_date'], p.get('num_days', 3), int(p.get('adults', 1)), p.get('currency', 'INR'))
    
    llm = get_llm(temperature=0.3)
    from prompts.templates import FLIGHT_AGENT_SYSTEM_PROMPT
    msg = [
        SystemMessage(content=FLIGHT_AGENT_SYSTEM_PROMPT),
        HumanMessage(content=json.dumps(raw_data))
    ]
    summary = invoke_with_retry(llm, msg).content
    return {"flight_results": summary, "raw_flight_results": raw_data}


def train_node(state: TravelPlanState) -> dict:
    p = state["parsed_input"]
    tc = TrainClient()
    raw_data = tc.search(p.get('origin_station_code', ''), p.get('destination_station_code', ''), p['departure_date'], p.get('num_days', 3))
    
    llm = get_llm(temperature=0.3)
    from prompts.templates import TRAIN_AGENT_SYSTEM_PROMPT
    msg = [
        SystemMessage(content=TRAIN_AGENT_SYSTEM_PROMPT),
        HumanMessage(content=json.dumps(raw_data))
    ]
    summary = invoke_with_retry(llm, msg).content
    return {"train_results": summary, "raw_train_results": raw_data}


def hotel_node(state: TravelPlanState) -> dict:
    p = state["parsed_input"]
    import datetime
    try:
        checkin = datetime.datetime.strptime(p['departure_date'], "%Y-%m-%d")
        checkout = checkin + datetime.timedelta(days=p.get('num_days', 3))
        checkout_date = checkout.strftime("%Y-%m-%d")
    except:
        checkout_date = p['departure_date']
        
    hc = HotelClient()
    raw_data = hc.search(p['destination_city'], p['departure_date'], checkout_date, p.get('adults', 1), p.get('children', 0), 7, p.get('currency', 'INR'))
    
    llm = get_llm(temperature=0.3)
    from prompts.templates import HOTEL_AGENT_SYSTEM_PROMPT
    msg = [
        SystemMessage(content=HOTEL_AGENT_SYSTEM_PROMPT),
        HumanMessage(content=json.dumps(raw_data))
    ]
    summary = invoke_with_retry(llm, msg).content
    return {"hotel_results": summary, "raw_hotel_results": raw_data}


def weather_node(state: TravelPlanState) -> dict:
    p = state["parsed_input"]
    wc = WeatherClient()
    raw_data = wc.search(p['destination_city'], p['departure_date'], p.get('num_days', 3))
    
    llm = get_llm(temperature=0.3)
    from prompts.templates import WEATHER_AGENT_SYSTEM_PROMPT
    msg = [
        SystemMessage(content=WEATHER_AGENT_SYSTEM_PROMPT),
        HumanMessage(content=json.dumps(raw_data))
    ]
    summary = invoke_with_retry(llm, msg).content
    return {"weather_results": summary, "raw_weather_results": raw_data}


def research_node(state: TravelPlanState) -> dict:
    p = state["parsed_input"]
    rc = ResearchClient()
    raw_data = rc.search(f"Best tourist attractions in {p['destination_city']}", 7)
    
    llm = get_llm(temperature=0.3)
    from prompts.templates import RESEARCH_AGENT_SYSTEM_PROMPT
    msg = [
        SystemMessage(content=RESEARCH_AGENT_SYSTEM_PROMPT),
        HumanMessage(content=json.dumps(raw_data))
    ]
    summary = invoke_with_retry(llm, msg).content
    return {"research_results": summary, "raw_research_results": raw_data}


def itinerary_node(state: TravelPlanState) -> dict:
    print("📋 [Itinerary Agent] Generating final travel plan...")
    p = state["parsed_input"]

    itinerary = generate_itinerary(
        flight_results=state.get("flight_results", "") + "\n" + state.get("train_results", ""),
        hotel_results=state.get("hotel_results", "No hotel data available"),
        weather_results=state.get("weather_results", "No weather data available"),
        research_results=state.get("research_results", "No research data available"),
        num_days=p.get("num_days", 3)
    )

    print("✅ [Itinerary Agent] Final plan generated!")
    return {"itinerary": itinerary}


# ============================================================
# ============================================================

def build_graph():
    builder = StateGraph(TravelPlanState)

    builder.add_node("coordinator", coordinator_node)
    builder.add_node("flight_agent", flight_node)
    builder.add_node("train_agent", train_node)
    builder.add_node("hotel_agent", hotel_node)
    builder.add_node("weather_agent", weather_node)
    builder.add_node("research_agent", research_node)
    builder.add_node("itinerary_agent", itinerary_node)

    builder.add_edge(START, "coordinator")

    def route_transport(state: TravelPlanState):
        pref = state["parsed_input"].get("preferred_transport", "flight").lower()
        if pref == "train":
            return ["train_agent", "hotel_agent", "weather_agent", "research_agent"]
        return ["flight_agent", "hotel_agent", "weather_agent", "research_agent"]

    builder.add_conditional_edges("coordinator", route_transport, ["flight_agent", "train_agent", "hotel_agent", "weather_agent", "research_agent"])

    builder.add_edge("flight_agent", "itinerary_agent")
    builder.add_edge("train_agent", "itinerary_agent")
    builder.add_edge("hotel_agent", "itinerary_agent")
    builder.add_edge("weather_agent", "itinerary_agent")
    builder.add_edge("research_agent", "itinerary_agent")

    builder.add_edge("itinerary_agent", END)

    graph = builder.compile(checkpointer=checkpointer)
    return graph


# ============================================================
# ============================================================

def run_travel_plan(user_query: str, thread_id: str = None) -> dict:
    graph = build_graph()
    if not thread_id:
        thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    initial_state = {
        "user_query": user_query,
        "parsed_input": {},
        "flight_results": "",
        "train_results": "",
        "hotel_results": "",
        "weather_results": "",
        "research_results": "",
        "raw_flight_results": {},
        "raw_train_results": {},
        "raw_hotel_results": {},
        "raw_weather_results": {},
        "raw_research_results": {},
        "itinerary": ""
    }
    result = graph.invoke(initial_state, config=config)
    return {
        "thread_id": thread_id,
        "parsed_input": result.get("parsed_input", {}),
        "flight_results": result.get("flight_results", ""),
        "train_results": result.get("train_results", ""),
        "hotel_results": result.get("hotel_results", ""),
        "weather_results": result.get("weather_results", ""),
        "research_results": result.get("research_results", ""),
        "raw_flight_results": result.get("raw_flight_results", {}),
        "raw_train_results": result.get("raw_train_results", {}),
        "raw_hotel_results": result.get("raw_hotel_results", {}),
        "raw_weather_results": result.get("raw_weather_results", {}),
        "raw_research_results": result.get("raw_research_results", {}),
        "itinerary": result.get("itinerary", "")
    }

import json

def run_travel_plan_stream(user_query: str, thread_id: str = None):
    graph = build_graph()
    if not thread_id:
        thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    initial_state = {
        "user_query": user_query,
        "parsed_input": {},
        "flight_results": "",
        "train_results": "",
        "hotel_results": "",
        "weather_results": "",
        "research_results": "",
        "raw_flight_results": {},
        "raw_train_results": {},
        "raw_hotel_results": {},
        "raw_weather_results": {},
        "raw_research_results": {},
        "itinerary": ""
    }
    
    yield {"agent": "system", "status": "Initializing workflow..."}
    
    final_state = initial_state.copy()
    for update in graph.stream(initial_state, config=config, stream_mode="updates"):
        for node_name, state_update in update.items():
            final_state.update(state_update)
            if node_name == "coordinator":
                yield {"agent": "coordinator", "status": "Parsed user query", "data": state_update.get("parsed_input")}
            elif node_name == "flight_agent":
                yield {"agent": "flight_agent", "status": "Flight search complete"}
            elif node_name == "train_agent":
                yield {"agent": "train_agent", "status": "Train search complete"}
            elif node_name == "hotel_agent":
                yield {"agent": "hotel_agent", "status": "Hotel search complete"}
            elif node_name == "weather_agent":
                yield {"agent": "weather_agent", "status": "Weather analysis complete"}
            elif node_name == "research_agent":
                yield {"agent": "research_agent", "status": "Attractions research complete"}
            elif node_name == "itinerary_agent":
                yield {"agent": "itinerary_agent", "status": "Final itinerary generated!"}

    yield {
        "agent": "complete",
        "status": "All tasks finished",
        "thread_id": thread_id,
        "parsed_input": final_state.get("parsed_input", {}),
        "flight_results": final_state.get("flight_results", ""),
        "train_results": final_state.get("train_results", ""),
        "hotel_results": final_state.get("hotel_results", ""),
        "weather_results": final_state.get("weather_results", ""),
        "research_results": final_state.get("research_results", ""),
        "raw_flight_results": final_state.get("raw_flight_results", {}),
        "raw_train_results": final_state.get("raw_train_results", {}),
        "raw_hotel_results": final_state.get("raw_hotel_results", {}),
        "raw_weather_results": final_state.get("raw_weather_results", {}),
        "raw_research_results": final_state.get("raw_research_results", {}),
        "itinerary": final_state.get("itinerary", "")
    }
