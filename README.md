# AI SDLC Platform - GHCP

This project is a Streamlit AI SDLC generator powered by GitHub Copilot through the Copilot SDK or local Copilot CLI instead of direct OpenAI API calls. It converts requirement documents into SDLC artifacts such as acceptance criteria, BDD scenarios, source code, test cases, and automation scripts.

The app keeps the human-in-the-loop workflow from the original AI SDLC project: users can review each stage, add feedback or additional instructions, regenerate outputs, and carry those decisions forward through Streamlit session state.

## Prerequisites

- Python 3.10+
- A GitHub token for a personal account with GitHub Copilot access
- Optional for local-only use: Node.js, npm, and GitHub Copilot CLI

Optional local CLI fallback:

```powershell
npm install -g @github/copilot
copilot login
```

## Run locally

```powershell
cd C:\Users\Kailash\OneDrive\Documents\AI_SDLC\GHCP_SDLC
pip install -r requirements.txt
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

## Configuration

The app does not require an OpenAI API key.

For Streamlit Community Cloud, open **App settings > Secrets** and add either:

```toml
SECRET_KEY = "github_pat_your_copilot_enabled_token"
```

or:

```toml
COPILOT_GITHUB_TOKEN = "github_pat_your_copilot_enabled_token"
```

For a `github_pat_...` fine-grained PAT, create it under the personal GitHub account that has Copilot access and grant the **Copilot Requests** account permission. A token can start with `github_pat_` and still fail if this permission or Copilot entitlement is missing.

Optional `.env` setting:

```text
SECRET_KEY=github_pat_your_copilot_enabled_token
GHCP_TIMEOUT_SECONDS=180
```

The app checks secrets in this order:

1. `COPILOT_GITHUB_TOKEN`
2. `GHCP_SDK_KEY`
3. `GHCP_TOKEN`
4. `SECRET_KEY`
5. Local `copilot` CLI fallback

## Deploy Notes

On Streamlit Community Cloud, use the SDK secret-based path. The first Copilot SDK request can take longer while the SDK runtime initializes.

For local execution, you can either use the same secret in `.env` or install and authenticate the local Copilot CLI.
