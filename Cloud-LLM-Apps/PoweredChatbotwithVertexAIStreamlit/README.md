# Gemini 2.5 Flash Chatbot — Streamlit

A conversational chatbot built with Streamlit and the Google Gemini API. Supports multi-turn conversation with full chat history, streaming responses, and a system prompt giving Gemini a helpful persona.

## Features

- Multi-turn conversation — Gemini remembers the full chat history
- Streaming responses for real-time output
- System prompt with clear persona and guidelines
- Clear chat button to reset the conversation
- Powered by Gemini 2.5 Flash via the Gemini API

## Tech Stack

- **Python** — application logic
- **Google Gemini API** — Gemini 2.5 Flash model
- **Streamlit** — web UI

## Setup

### Step 1 — Get a Gemini API key

1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Click **Create API key**
3. Copy the key

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

Copy `.env.example` to `.env` and fill in your API key:

```bash
cp .env.example .env
```

```ini
GEMINI_API_KEY=your-gemini-api-key
```

### Step 5 — Run the app

```bash
streamlit run main.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.
