
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemas.models import TravelQuery
from prompts.templates import COORDINATOR_SYSTEM_PROMPT
from agents.llm_utils import get_llm, invoke_with_retry
from dotenv import load_dotenv

load_dotenv()


def parse_user_query(user_query: str) -> dict:
    llm = get_llm(temperature=0)
    structured_llm = llm.with_structured_output(TravelQuery)

    result = invoke_with_retry(
        structured_llm,
        f"{COORDINATOR_SYSTEM_PROMPT}\n\nUser Query: {user_query}"
    )

    return result.model_dump()
