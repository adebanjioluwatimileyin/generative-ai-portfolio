# LLM-Powered Chatbot with Vertex AI

A Flask web chatbot powered by Google Gemini 1.5 Flash via Vertex AI. Features a dark-themed chat UI with conversation history.

## How It Works

```
User message → Flask backend → Gemini 1.5 Flash (Vertex AI) → Response displayed in chat
```

## Features

- Gemini 1.5 Flash via Google Vertex AI
- Chat bubble UI with full conversation history
- "Thinking..." indicator while waiting for response
- Send with Enter key or button click
- Dark themed responsive UI

## Setup

### 1. Create and activate a conda environment

```bash
conda create -n chatbot python=3.11 -y
conda activate chatbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up Google Cloud credentials

Install the Google Cloud CLI:
```bash
# macOS
brew install google-cloud-sdk

# or download from: https://cloud.google.com/sdk/docs/install
```

Authenticate:
```bash
gcloud auth application-default login
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```
project_id=your-gcp-project-id
region=us-central1
```

Enable the Vertex AI API in your GCP project:
```bash
gcloud services enable aiplatform.googleapis.com
```

### 5. Run the app

```bash
python app.py
```

Opens at `http://localhost:8080`.

## Tech Stack

- [Flask](https://flask.palletsprojects.com/) — web framework
- [Google Vertex AI](https://cloud.google.com/vertex-ai) — Gemini 1.5 Flash model
- Vanilla JS — frontend chat UI
