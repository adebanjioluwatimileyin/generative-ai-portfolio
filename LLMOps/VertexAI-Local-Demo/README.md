# VertexAI Local Demo

A minimal Streamlit app to interact with Google Gemini 1.5 Flash via Vertex AI from your local machine.

## Tech Stack

- **Python** — application logic
- **Vertex AI** — Gemini 1.5 Flash model
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
