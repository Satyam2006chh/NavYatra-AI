"""
Itinerary Agent — Synthesizes all agent outputs into a final travel plan.
Uses LLM chain (no tools) since it reasons over already-collected data.
Truncates inputs to stay within Groq free-tier token limits.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.prompts import ChatPromptTemplate
from prompts.templates import ITINERARY_SYNTHESIS_PROMPT
from agents.llm_utils import get_llm, invoke_with_retry, truncate_output
from dotenv import load_dotenv

load_dotenv()


def create_itinerary_chain():
    """Create the final itinerary synthesis chain."""
    llm = get_llm(temperature=0.7)
    prompt = ChatPromptTemplate.from_template(ITINERARY_SYNTHESIS_PROMPT)
    chain = prompt | llm
    return chain


def generate_itinerary(flight_results: str, hotel_results: str,
                       weather_results: str, research_results: str,
                       num_days: int = 3) -> str:
    """Generate the final travel itinerary from all agent outputs.

    Truncates each agent's output to stay within token limits.
    """
    chain = create_itinerary_chain()

    result = invoke_with_retry(chain, {
        "flight_results": truncate_output(flight_results),
        "hotel_results": truncate_output(hotel_results),
        "weather_results": truncate_output(weather_results),
        "research_results": truncate_output(research_results),
        "num_days": num_days
    })

    return result.content
