"""
Weather Agent — Uses LLM tool-calling with retry logic for rate limits.
"""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from api.weather import WeatherClient
from prompts.templates import WEATHER_AGENT_SYSTEM_PROMPT
from agents.llm_utils import get_llm, invoke_with_retry
from dotenv import load_dotenv

load_dotenv()


@tool
def search_weather(city_name: str) -> str:
    """Get current weather and forecast for a city.

    Args:
        city_name: The city to check weather for (e.g. Goa, Manali, Delhi)

    Returns:
        JSON string with current temperature, humidity, wind, and 5-day forecast.
    """
    client = WeatherClient()
    result = client.search(city_name)
    return json.dumps(result, indent=2)


def run_weather_agent(input_text: str) -> str:
    """Run the Weather Agent with retry logic."""
    llm = get_llm(temperature=0.3)
    tools = [search_weather]
    llm_with_tools = llm.bind_tools(tools)

    messages = [
        SystemMessage(content=WEATHER_AGENT_SYSTEM_PROMPT),
        HumanMessage(content=input_text)
    ]

    response = invoke_with_retry(llm_with_tools, messages)
    messages.append(response)

    if response.tool_calls:
        for tc in response.tool_calls:
            tool_result = search_weather.invoke(tc["args"])
            messages.append(ToolMessage(content=tool_result, tool_call_id=tc["id"]))

        final_response = invoke_with_retry(llm_with_tools, messages)
        return final_response.content
    else:
        return response.content
