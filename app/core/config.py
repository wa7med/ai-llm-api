import os

class Config:
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
