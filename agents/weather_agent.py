
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
