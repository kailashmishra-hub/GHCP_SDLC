from __future__ import annotations

import asyncio
import os
import tempfile
from pathlib import Path


def _validate_token(token: str) -> None:
    if token.startswith("ghp_"):
        raise RuntimeError(
            "GitHub classic PAT tokens (ghp_) are not supported by the Copilot SDK. "
            "Use a fine-grained PAT (github_pat_) or a GitHub OAuth/App user token (gho_ or ghu_) "
            "from a GitHub account with Copilot access."
        )
    if token.startswith("ghs_"):
        raise RuntimeError(
            "GitHub App installation tokens (ghs_) expire quickly and cannot be used as a static "
            "Streamlit secret. Use a fine-grained PAT (github_pat_) or user token (gho_ or ghu_), "
            "or mint a fresh installation token per request."
        )


def _copilot_auth_hint() -> str:
    return (
        "GitHub Copilot authorization failed. If you are using a fine-grained PAT, create it "
        "from your personal GitHub account, make sure that account has active Copilot access, "
        "and grant the token the 'Copilot Requests' account permission. Then set it as "
        "COPILOT_GITHUB_TOKEN in Streamlit Secrets and reboot the app."
    )


async def _generate_with_sdk(prompt: str, github_token: str, timeout_seconds: int) -> str:
    try:
        from copilot import CopilotClient
        from copilot.session import PermissionHandler
    except ImportError as exc:
        raise RuntimeError(
            "The GitHub Copilot SDK is not installed. Add github-copilot-sdk to requirements.txt."
        ) from exc

    runtime_directory = Path(tempfile.gettempdir()) / "ghcp-sdlc-copilot-runtime"
    runtime_directory.mkdir(parents=True, exist_ok=True)
    os.environ["COPILOT_GITHUB_TOKEN"] = github_token
    os.environ["COPILOT_BASE_DIRECTORY"] = str(runtime_directory)
    client = CopilotClient()
    session = None
    try:
        await client.start()
        session = await client.create_session(
            available_tools=[],
            on_permission_request=PermissionHandler.approve_all,
        )
        response = await session.send_and_wait(prompt, timeout=timeout_seconds)
        content = getattr(getattr(response, "data", None), "content", None)
        if not content or not content.strip():
            raise RuntimeError("GitHub Copilot returned an empty response.")
        return content.strip()
    finally:
        if session is not None:
            await session.disconnect()
        await client.stop()


def generate_copilot_text(prompt: str, github_token: str, timeout_seconds: int = 180) -> str:
    token = github_token.strip()
    if not token:
        raise RuntimeError("GitHub Copilot token is not configured in Streamlit Secrets.")
    _validate_token(token)
    try:
        return asyncio.run(_generate_with_sdk(prompt, token, timeout_seconds))
    except Exception as exc:
        message = str(exc)
        auth_markers = (
            "Authorization error",
            "credentials may be expired or invalid",
            "No GitHub OAuth token or Copilot HMAC key provided",
            "Bad credentials",
            "Not authenticated",
        )
        if any(marker in message for marker in auth_markers):
            raise RuntimeError(f"{_copilot_auth_hint()} Original error: {message}") from exc
        raise
