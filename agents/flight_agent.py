"""
Flight Agent — Uses LLM tool-calling with retry logic.
Includes fallback for Cerebras compatibility.
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
    """Run the Flight Agent with retry logic and Cerebras fallback."""
    llm = get_llm(temperature=0.3)
    tools = [search_flights]
    llm_with_tools = llm.bind_tools(tools)

    messages = [
        SystemMessage(content=FLIGHT_AGENT_SYSTEM_PROMPT),
        HumanMessage(content=input_text)
    ]

    try:
        response = invoke_with_retry(llm_with_tools, messages)
        messages.append(response)

        if response.tool_calls:
            tc = response.tool_calls[0]
            tool_result = search_flights.invoke(tc["args"])
            messages.append(ToolMessage(content=tool_result, tool_call_id=tc["id"]))

            final_response = invoke_with_retry(llm_with_tools, messages)
            return final_response.content
        else:
            return response.content

    except Exception as e:
        error_str = str(e)
        if "tool_use_failed" in error_str and "failed_generation" in error_str:
            print("⚠️  [Flight Agent] Cerebras tool error, using fallback...")
            llm_plain = get_llm(temperature=0.3)
            fallback_messages = [
                SystemMessage(content=FLIGHT_AGENT_SYSTEM_PROMPT),
                HumanMessage(content=input_text + "\n\nNote: The flight search tool is temporarily unavailable. Please provide helpful alternative transport suggestions based on your knowledge.")
            ]
            fallback_response = invoke_with_retry(llm_plain, fallback_messages)
            return fallback_response.content
        raise e
