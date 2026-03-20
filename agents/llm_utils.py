"""
LLM Utilities — Cerebras-powered LLM with retry logic.
Migrated from Groq to Cerebras for higher rate limits (1M TPD).
"""

import time
import os
from langchain_cerebras import ChatCerebras
from dotenv import load_dotenv

load_dotenv()


def get_llm(temperature: float = 0.3):
    """Get a ChatCerebras LLM instance."""
    return ChatCerebras(
        model="llama3.1-8b",
        api_key=os.getenv("CEREBRAS_API_KEY"),
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
                wait_time = 10 * (attempt + 1)  # 10s, 20s, 30s
                print(f"⏳ Rate limit hit. Waiting {wait_time}s before retry ({attempt + 1}/{max_retries})...")
                time.sleep(wait_time)
            else:
                raise e

    raise Exception("Max retries exceeded")
