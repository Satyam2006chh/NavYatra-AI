"""
Hotel Agent — Uses LLM tool-calling with retry logic for rate limits.
"""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from api.hotels import HotelClient
from prompts.templates import HOTEL_AGENT_SYSTEM_PROMPT
from agents.llm_utils import get_llm, invoke_with_retry
from dotenv import load_dotenv

load_dotenv()


@tool
def search_hotels(city_name: str, limit: int = 7) -> str:
    """Search for hotels in a specific city.

    Args:
        city_name: The city to search hotels in (e.g. Goa, Manali, Jaipur)
        limit: Maximum number of hotels to return

    Returns:
        JSON string with hotel names, addresses, and coordinates.
    """
    client = HotelClient()
    result = client.search(city_name, limit)
    return json.dumps(result, indent=2)


def run_hotel_agent(input_text: str) -> str:
    """Run the Hotel Agent with retry logic."""
    llm = get_llm(temperature=0.3)
    tools = [search_hotels]
    llm_with_tools = llm.bind_tools(tools)

    messages = [
        SystemMessage(content=HOTEL_AGENT_SYSTEM_PROMPT),
        HumanMessage(content=input_text)
    ]

    response = invoke_with_retry(llm_with_tools, messages)
    messages.append(response)

    if response.tool_calls:
        for tc in response.tool_calls:
            tool_result = search_hotels.invoke(tc["args"])
            messages.append(ToolMessage(content=tool_result, tool_call_id=tc["id"]))

        final_response = invoke_with_retry(llm_with_tools, messages)
        return final_response.content
    else:
        return response.content
