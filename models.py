"""Какая модель стоит за агентом. Настройки читаются из переменных окружения (образец — .env.example)."""

import os
from pathlib import Path

from agents import OpenAIChatCompletionsModel, set_tracing_disabled
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv(Path(__file__).resolve().parent / ".env")  # .env лежит рядом с кодом, а не в папке прогона
set_tracing_disabled(True)  # трассы SDK уходят в OpenAI; наш журнал — journal.jsonl


def build_model():
    provider = os.getenv("MODEL_PROVIDER", "openai")
    if provider == "openai":
        return os.getenv("OPENAI_MODEL", "gpt-5.6-luna")  # SDK сам возьмёт OPENAI_API_KEY
    if provider == "ollama":
        client = AsyncOpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
        return OpenAIChatCompletionsModel(model=os.environ["OLLAMA_MODEL"], openai_client=client)
    if provider == "hf":
        client = AsyncOpenAI(base_url="https://router.huggingface.co/v1", api_key=os.environ["HF_TOKEN"])
        return OpenAIChatCompletionsModel(model=os.environ["HF_MODEL"], openai_client=client)
    raise ValueError(f"Неизвестный MODEL_PROVIDER: {provider} (бывает openai, ollama или hf)")
