"""
Flight Agent — Uses LLM tool-calling with retry logic for rate limits.
"""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from api.flights import FlightClient
from prompts.templates import FLIGHT_AGENT_SYSTEM_PROMPT
from agents.llm_utils import get_llm, invoke_with_retry
from dotenv import load_dotenv

load_dotenv()


@tool
def search_flights(origin_city: str, destination_city: str,
                   departure_date: str, adults: str = "1",
                   currency: str = "INR") -> str:
    """Search for available flights between two cities on a specific date.

    Args:
        origin_city: The departure city name (e.g. Delhi, Mumbai)
        destination_city: The destination city name (e.g. Goa, Manali)
        departure_date: Date in YYYY-MM-DD format
        adults: Number of adult travelers as a string (e.g. "1", "2")
        currency: Currency code (INR, USD, EUR)

    Returns:
        JSON string with available flight options including airlines, times, and prices.
    """
    client = FlightClient()
    result = client.search(origin_city, destination_city, departure_date, int(adults), currency)
    return json.dumps(result, indent=2)


def run_flight_agent(input_text: str) -> str:
    """Run the Flight Agent with retry logic."""
    llm = get_llm(temperature=0.3)
    tools = [search_flights]
    llm_with_tools = llm.bind_tools(tools)

    messages = [
        SystemMessage(content=FLIGHT_AGENT_SYSTEM_PROMPT),
        HumanMessage(content=input_text)
    ]

    response = invoke_with_retry(llm_with_tools, messages)
    messages.append(response)

    if response.tool_calls:
        for tc in response.tool_calls:
            tool_result = search_flights.invoke(tc["args"])
            messages.append(ToolMessage(content=tool_result, tool_call_id=tc["id"]))

        final_response = invoke_with_retry(llm_with_tools, messages)
        return final_response.content
    else:
        return response.content
