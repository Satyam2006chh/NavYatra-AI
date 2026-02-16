"""
Weather Agent — Uses LLM tool-calling with retry logic.
Includes fallback for Cerebras compatibility.
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
    """Run the Weather Agent with retry logic and Cerebras fallback."""
    llm = get_llm(temperature=0.3)
    tools = [search_weather]
    llm_with_tools = llm.bind_tools(tools)

    messages = [
        SystemMessage(content=WEATHER_AGENT_SYSTEM_PROMPT),
        HumanMessage(content=input_text)
    ]

    try:
        response = invoke_with_retry(llm_with_tools, messages)
        messages.append(response)

        if response.tool_calls:
            tc = response.tool_calls[0]
            tool_result = search_weather.invoke(tc["args"])
            messages.append(ToolMessage(content=tool_result, tool_call_id=tc["id"]))

            final_response = invoke_with_retry(llm_with_tools, messages)
            return final_response.content
        else:
            return response.content

    except Exception as e:
        error_str = str(e)
        if "tool_use_failed" in error_str and "failed_generation" in error_str:
            print("⚠️  [Weather Agent] Cerebras tool error, using fallback...")
            llm_plain = get_llm(temperature=0.3)
            fallback_messages = [
                SystemMessage(content=WEATHER_AGENT_SYSTEM_PROMPT),
                HumanMessage(content=input_text + "\n\nNote: The weather tool is temporarily unavailable. Please provide general weather guidance based on your knowledge of this destination and time of year.")
            ]
            fallback_response = invoke_with_retry(llm_plain, fallback_messages)
            return fallback_response.content
        raise e
