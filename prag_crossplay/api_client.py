from __future__ import annotations

import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ApiResult:
    text: str
    data: dict[str, Any]
    cached: bool
    usage: dict[str, Any]
    cache_path: str


class OpenAIResponsesClient:
    def __init__(
        self,
        api_key_path: str = "/home/eston/colm_workshop/apikey.txt",
        cache_dir: str = "data/cached_responses",
        model: str = "gpt-5.4-nano",
        temperature: float = 0.0,
        timeout: int = 60,
    ) -> None:
        self.api_key_path = Path(api_key_path)
        self.cache_dir = Path(cache_dir)
        self.model = model
        self.temperature = temperature
        self.timeout = timeout
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def call(
        self,
        system: str,
        user: str,
        max_output_tokens: int = 300,
        schema_version: str = "v1",
    ) -> ApiResult:
        key_payload = {
            "provider": "openai",
            "endpoint": "responses",
            "model": self.model,
            "temperature": self.temperature,
            "system": system,
            "user": user,
            "max_output_tokens": max_output_tokens,
            "schema_version": schema_version,
        }
        cache_path = self.cache_dir / f"{_hash(key_payload)}.json"
        if cache_path.exists():
            cached = json.loads(cache_path.read_text(encoding="utf-8"))
            return ApiResult(
                text=cached["text"],
                data=cached["data"],
                cached=True,
                usage=cached.get("usage", {}),
                cache_path=str(cache_path),
            )

        api_key = self._read_api_key()
        payload: dict[str, Any] = {
            "model": self.model,
            "input": [
                {"role": "developer", "content": system},
                {"role": "user", "content": user},
            ],
            "max_output_tokens": max_output_tokens,
        }
        if self.temperature is not None:
            payload["temperature"] = self.temperature

        req = urllib.request.Request(
            "https://api.openai.com/v1/responses",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"OpenAI API HTTP {exc.code}: {body}") from exc

        text = _response_text(data)
        cached = {
            "created_at": time.time(),
            "text": text,
            "data": data,
            "usage": data.get("usage", {}),
            "request_hash_payload": key_payload,
        }
        cache_path.write_text(json.dumps(cached, indent=2, sort_keys=True), encoding="utf-8")
        return ApiResult(
            text=text,
            data=data,
            cached=False,
            usage=data.get("usage", {}),
            cache_path=str(cache_path),
        )

    def call_json(
        self,
        system: str,
        user: str,
        max_output_tokens: int = 300,
        schema_version: str = "v1",
    ) -> tuple[dict[str, Any], ApiResult]:
        result = self.call(system, user, max_output_tokens=max_output_tokens, schema_version=schema_version)
        return parse_json_object(result.text), result

    def _read_api_key(self) -> str:
        if "OPENAI_API_KEY" in os.environ:
            return os.environ["OPENAI_API_KEY"].strip()
        return self.api_key_path.read_text(encoding="utf-8").strip()


def parse_json_object(text: str) -> dict[str, Any]:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{.*\}", text, flags=re.S)
    if not match:
        raise ValueError(f"no JSON object found in response: {text[:200]!r}")
    return json.loads(match.group(0))


def _response_text(data: dict[str, Any]) -> str:
    if isinstance(data.get("output_text"), str):
        return data["output_text"]
    chunks: list[str] = []
    for item in data.get("output", []):
        for content in item.get("content", []):
            if isinstance(content, dict):
                if isinstance(content.get("text"), str):
                    chunks.append(content["text"])
                elif isinstance(content.get("output_text"), str):
                    chunks.append(content["output_text"])
    return "\n".join(chunks).strip()


def _hash(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()
