# OpenAI Demo

Jupyter notebooks demonstrating core OpenAI API features — chat completions, prompt engineering, function calling, and more.

## Tech Stack

- **Python** — application logic
- **OpenAI API** — GPT models

## Setup

### Step 1 — Create and activate a conda environment

```bash
conda create -n openai-demo python=3.10 -y
conda activate openai-demo
```

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Set up environment variables

Copy `.env.example` to `.env` and fill in your key:

```bash
cp .env.example .env
```

```ini
OPENAI_API_KEY=your_openai_api_key_here
```

### Step 4 — Launch Jupyter

```bash
jupyter notebook
```

## Notebooks

- `openaidemo1.ipynb` — Chat completions, prompt engineering basics
- `openaidemo2.ipynb` — Advanced API features and experiments
