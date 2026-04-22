# Gemini 2.0 Flash Chatbot — Vertex AI + Streamlit

A conversational chatbot built with Streamlit and Google Vertex AI. Supports multi-turn conversation with full chat history, streaming responses, and a system prompt giving Gemini a helpful persona.

## Features

- Multi-turn conversation — Gemini remembers the full chat history
- Streaming responses for real-time output
- System prompt with clear persona and guidelines
- Clear chat button to reset the conversation
- Powered by Gemini 2.0 Flash via Vertex AI

## Tech Stack

- **Python** — application logic
- **Vertex AI** — Gemini 2.0 Flash model
- **Streamlit** — web UI

## Setup

### Step 1 — Authenticate with Google Cloud

```bash
gcloud auth application-default login
```

### Step 2 — Create and activate a conda environment

```bash
conda create -n vertexai-demo python=3.10 -y
conda activate vertexai-demo
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Set up environment variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

```ini
project_id=your_gcp_project_id
region=us-central1
```

### Step 5 — Run the app

```bash
streamlit run main.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.
