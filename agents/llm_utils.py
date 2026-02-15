"""
LLM Utilities — Rate limit handling, retries, and token management.
"""

import time
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

# Max characters to keep from each agent's output before sending to itinerary
MAX_AGENT_OUTPUT_CHARS = 2000


def get_llm(temperature: float = 0.3):
    """Get a ChatGroq LLM instance."""
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=temperature
    )


def invoke_with_retry(llm_or_chain, input_data, max_retries=3):
    """Invoke an LLM/chain with retry logic for rate limit errors.

    Catches rate limit (429/413) errors and retries with exponential backoff.
    """
    for attempt in range(max_retries):
        try:
            return llm_or_chain.invoke(input_data)

        except Exception as e:
            error_str = str(e).lower()
            is_rate_limit = any(keyword in error_str for keyword in [
                "rate_limit", "429", "413", "too large", "tokens per minute",
                "requests per minute", "rate limit"
            ])

            if is_rate_limit and attempt < max_retries - 1:
                wait_time = 15 * (attempt + 1)  # 15s, 30s, 45s
                print(f"⏳ Rate limit hit. Waiting {wait_time}s before retry ({attempt + 1}/{max_retries})...")
                time.sleep(wait_time)
            else:
                raise e

    raise Exception("Max retries exceeded")


def truncate_output(text: str, max_chars: int = MAX_AGENT_OUTPUT_CHARS) -> str:
    """Truncate agent output to stay within token limits."""
    if not text or len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n\n... (truncated for brevity)"
