from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    project_name: str
    technology_stack: str
    automation_framework: str
    output_directory: Path
    ghcp_timeout_seconds: int = 180
    astra_endpoint: str = ""
    astra_token: str = ""
    astra_collection: str = "ai_sdlc_documents"
