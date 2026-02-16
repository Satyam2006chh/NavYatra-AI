"""
Research Agent — Uses LLM tool-calling with retry logic for rate limits.
"""

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
        JSON string with titles, URLs, and content about the destination.
    """
    client = ResearchClient()
    result = client.search(query, 5)
    return json.dumps(result, indent=2)


def run_research_agent(input_text: str) -> str:
    """Run the Research Agent with retry logic."""
    llm = get_llm(temperature=0.3)
    tools = [search_attractions]
    llm_with_tools = llm.bind_tools(tools)

    messages = [
        SystemMessage(content=RESEARCH_AGENT_SYSTEM_PROMPT),
        HumanMessage(content=input_text)
    ]

    response = invoke_with_retry(llm_with_tools, messages)
    messages.append(response)

    if response.tool_calls:
        for tc in response.tool_calls:
            tool_result = search_attractions.invoke(tc["args"])
            messages.append(ToolMessage(content=tool_result, tool_call_id=tc["id"]))

        final_response = invoke_with_retry(llm_with_tools, messages)
        return final_response.content
    else:
        return response.content
