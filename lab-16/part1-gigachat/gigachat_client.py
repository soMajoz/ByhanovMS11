"""Small GigaChat API client used in lab 16."""

from __future__ import annotations

import json
import os
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import requests
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


@dataclass
class GigaChatConfig:
    credentials: str
    scope: str = "GIGACHAT_API_PERS"
    model: str = "GigaChat"
    verify_ssl: bool = False
    auth_url: str = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    chat_url: str = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    @classmethod
    def from_env(cls) -> "GigaChatConfig":
        credentials = os.getenv("GIGACHAT_CREDENTIALS", "").strip()
        if not credentials:
            raise RuntimeError("GIGACHAT_CREDENTIALS is not set. Copy .env.example to .env and fill it.")
        verify_ssl = os.getenv("GIGACHAT_VERIFY_SSL", "false").lower() in {"1", "true", "yes"}
        return cls(
            credentials=credentials,
            scope=os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS"),
            model=os.getenv("GIGACHAT_MODEL", "GigaChat"),
            verify_ssl=verify_ssl,
        )


class GigaChatClient:
    def __init__(self, config: GigaChatConfig | None = None):
        self.config = config or GigaChatConfig.from_env()
        self._access_token: str | None = None

    def get_access_token(self) -> str:
        if self._access_token:
            return self._access_token

        response = requests.post(
            self.config.auth_url,
            headers={
                "Authorization": f"Basic {self.config.credentials}",
                "RqUID": str(uuid.uuid4()),
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={"scope": self.config.scope},
            timeout=30,
            verify=self.config.verify_ssl,
        )
        response.raise_for_status()
        self._access_token = response.json()["access_token"]
        return self._access_token

    def chat(self, prompt: str, system_prompt: str = "Ты полезный ассистент разработчика.") -> str:
        token = self.get_access_token()
        response = requests.post(
            self.config.chat_url,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            json={
                "model": self.config.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.2,
            },
            timeout=60,
            verify=self.config.verify_ssl,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    @staticmethod
    def strip_markdown_code_block(text: str) -> str:
        lines = text.strip().splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        return "\n".join(lines).strip()


def save_text(path: str | Path, content: str) -> None:
    Path(path).write_text(content, encoding="utf-8")


def run_generation(prompts: Iterable[tuple[str, Path]]) -> None:
    client = GigaChatClient()
    for prompt, target in prompts:
        answer = client.chat(prompt)
        save_text(target, client.strip_markdown_code_block(answer))


if __name__ == "__main__":
    prompts = [
        (
            "Напиши на Python функции is_prime(n), fibonacci(n), normalize_phone(phone) с docstring и type hints.",
            BASE_DIR / "generated_code.py",
        ),
        (
            "Создай README на русском для проекта с функциями is_prime, fibonacci и normalize_phone.",
            BASE_DIR / "README_generated.md",
        ),
    ]
    run_generation(prompts)
    print(json.dumps({"generated": [str(path.name) for _, path in prompts]}, ensure_ascii=False))

