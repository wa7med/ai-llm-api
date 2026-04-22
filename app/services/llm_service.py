import requests
import json
import os
from dotenv import load_dotenv
from app.schemas.request_response import OutputResponse

load_dotenv()

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

PROVIDERS = ["ollama", "openrouter", "openai"]


def call_llm(prompt: str) -> dict:
    configured = os.getenv("LLM_PROVIDER", "ollama")
    provider_order = [configured]
    # Append fallback providers that differ from the primary
    for p in PROVIDERS:
        if p != configured:
            provider_order.append(p)

    raw = None
    active_provider = configured

    for provider in provider_order:
        try:
            raw = _call_provider(provider, prompt)
            active_provider = provider
            break
        except Exception as e:
            print(f"Provider {provider} failed: {e}")
            continue

    if raw is None:
        return {"provider": "none", "error": "all_providers_failed"}

    parsed = safe_parse(raw)
    validated = OutputResponse(**parsed)
    return {"provider": active_provider, **validated.dict()}


def _call_provider(provider: str, prompt: str) -> str:
    if provider == "ollama":
        response = requests.post(
            os.getenv("OLLAMA_BASE_URL", "http://localhost:11434") + "/api/generate",
            json={
                "model": os.getenv("OLLAMA_MODEL", "llama3"),
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json().get("response", "")

    elif provider == "openrouter":
        response = requests.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
                "Content-Type": "application/json"
            },
            json={
                "model": os.getenv("OPENROUTER_MODEL", "openrouter/free"),
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        data = response.json()
        if "error" in data:
            raise RuntimeError(f"OpenRouter error: {data['error']}")
        return data["choices"][0]["message"]["content"]

    elif provider == "openai":
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    raise ValueError(f"Unknown provider: {provider}")


def safe_parse(output: str) -> dict:
    text = output.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)
    return json.loads(text)
