"""
LangGraph State Definition for NavYatra AI.
Defines the shared state that flows through the graph.
"""

from typing import TypedDict, Optional


class TravelPlanState(TypedDict):
    """State schema for the travel planning graph."""

    # Input
    user_query: str

    # Coordinator output
    parsed_input: dict

    # Agent outputs (each agent writes to its own key)
    flight_results: str
    hotel_results: str
    weather_results: str
    research_results: str

    # Final synthesis
    itinerary: str
