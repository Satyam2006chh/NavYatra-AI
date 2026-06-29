
import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from api.research import ResearchClient
from prompts.templates import RESEARCH_AGENT_SYSTEM_PROMPT
from agents.llm_utils import get_llm, invoke_with_retry
from dotenv import load_dotenv

load_dotenv()


@tool
def search_attractions(query: str) -> str:
    """Search for tourist attractions, local tips, and travel information about a destination.

    Args:
        query: Search query about the destination (e.g. "Best tourist attractions in Goa")

    Returns:
        JSON string with titles, ratings, reviews, and addresses of attractions.
