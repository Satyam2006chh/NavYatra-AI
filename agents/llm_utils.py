
import time
import os
from langchain_cerebras import ChatCerebras
from dotenv import load_dotenv

load_dotenv()


def get_llm(temperature: float = 0.3):
    return ChatCerebras(
        model="gpt-oss-120b",
        api_key=os.getenv("CEREBRAS_API_KEY"),
        temperature=temperature,
        max_tokens=4096
    )


def invoke_with_retry(llm_or_chain, input_data, max_retries=3):
    """Invoke an LLM/chain with retry logic for rate limit errors.

    Catches rate limit (429/413) errors and retries with exponential backoff.
