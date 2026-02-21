"""OpenRouter API client setup."""

import os

from openai import OpenAI

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")
MODEL = "anthropic/claude-haiku-4.5"


def create_client() -> OpenAI:
    """Create and return an authenticated OpenAI client."""
    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")
    return OpenAI(api_key=API_KEY, base_url=BASE_URL)
