from __future__ import annotations

import asyncio
import tempfile
from pathlib import Path


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
    client = CopilotClient(
        mode="empty",
        base_directory=str(runtime_directory),
        github_token=github_token,
        use_logged_in_user=False,
    )
    session = None
    try:
        await client.start()
        session = await client.create_session(
            github_token=github_token,
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
    return asyncio.run(_generate_with_sdk(prompt, token, timeout_seconds))
