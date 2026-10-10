from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from typing import Any

from ai_sdlc.config import AppConfig
from copilot_service import generate_copilot_text


class LLMClient:
    def __init__(self, config: AppConfig):
        self.config = config
        self._copilot = shutil.which("copilot")
        self._token = (
            config.copilot_github_token
            or os.getenv("COPILOT_GITHUB_TOKEN", "")
            or os.getenv("GHCP_SDK_KEY", "")
            or os.getenv("GHCP_TOKEN", "")
            or os.getenv("SECRET_KEY", "")
        ).strip()

    @property
    def enabled(self) -> bool:
        return bool(self._token or self._copilot)

    def invoke_text(self, system: str, user: str) -> str | None:
        prompt = (
            f"System instructions:\n{system.strip()}\n\n"
            f"User request:\n{user.strip()}\n\n"
            "Return only the requested artifact content. Do not ask follow-up questions."
        )
        if self._token:
            try:
                return generate_copilot_text(prompt, self._token, self.config.ghcp_timeout_seconds)
            except Exception:
                return None
        if not self._copilot:
            return None
        try:
            response = subprocess.run(
                [
                    self._copilot,
                    "--no-color",
                    "--no-ask-user",
                    "--no-custom-instructions",
                    "--deny-tool=shell",
                    "--deny-tool=write",
                    "--deny-tool=read",
                    "--deny-tool=url",
                ],
                cwd=tempfile.gettempdir(),
                input=prompt,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=self.config.ghcp_timeout_seconds,
                check=False,
            )
        except Exception:
            return None
        if response.returncode != 0 or not response.stdout.strip():
            return None
        return response.stdout.strip()

    def invoke_json(self, system: str, user: str) -> dict[str, Any] | None:
        text = self.invoke_text(system, user)
        if not text:
            return None
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            cleaned = cleaned.removeprefix("json").strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return None
