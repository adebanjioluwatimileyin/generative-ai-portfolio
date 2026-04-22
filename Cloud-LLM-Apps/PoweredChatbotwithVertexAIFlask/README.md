# LLM-Powered Chatbot with Flask

A Flask web chatbot powered by Google Gemini 2.5 Flash via the Gemini API. Features a dark-themed chat UI with full conversation history, markdown rendering, streaming-style responses, and multi-turn memory.

## How It Works

```
User message → Flask backend → Gemini 2.5 Flash (Gemini API) → Response displayed in chat
```

## Features

- Gemini 2.5 Flash via the Google Gemini API
- Multi-turn conversation — Gemini remembers the full chat history per session
- Markdown rendering in bot responses (code blocks, lists, bold text)
- Animated typing indicator while waiting for a response
- Auto-resize textarea with Shift+Enter for new lines
- Clear chat button to reset the conversation
- Dark themed responsive UI

## Setup

### 1. Get a Gemini API key

1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Click **Create API key**
3. Copy the key

### 2. Create and activate a conda environment

```bash
conda create -n chatbot python=3.11 -y
conda activate chatbot
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```ini
GEMINI_API_KEY=your-gemini-api-key
flask_secret_key=your-random-secret-key
```

To generate a secure secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 5. Run the app

```bash
python app.py
```

Opens at `http://localhost:8080`.

## Tech Stack

- [Flask](https://flask.palletsprojects.com/) — web framework
- [Google Gemini API](https://ai.google.dev/) — Gemini 2.5 Flash model
- Vanilla JS + marked.js — frontend chat UI
