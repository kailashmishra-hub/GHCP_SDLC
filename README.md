# AI SDLC Platform - GHCP

This project is a Streamlit AI SDLC generator powered by GitHub Copilot CLI instead of direct OpenAI API calls. It converts requirement documents into SDLC artifacts such as acceptance criteria, BDD scenarios, source code, test cases, and automation scripts.

The app keeps the human-in-the-loop workflow from the original AI SDLC project: users can review each stage, add feedback or additional instructions, regenerate outputs, and carry those decisions forward through Streamlit session state.

## Prerequisites

- Python 3.10+
- Node.js and npm
- GitHub Copilot CLI authenticated on the machine running the app

Install and authenticate GitHub Copilot CLI:

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

The app does not require an OpenAI API key. It invokes the local `copilot` CLI in non-interactive mode.

Optional `.env` setting:

```text
GHCP_TIMEOUT_SECONDS=180
```

## Deploy Notes

This app depends on the GitHub Copilot CLI being installed and authenticated in the runtime environment. It is best suited for local execution or an environment where Copilot CLI authentication is supported.

For Streamlit Community Cloud, verify whether your target runtime can install and authenticate the Copilot CLI before deploying.
