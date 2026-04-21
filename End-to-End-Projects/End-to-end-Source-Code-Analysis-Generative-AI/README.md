# End-to-End Source Code Analysis — Generative AI

An AI-powered tool to analyze GitHub repositories. Paste any public repo URL, let the app clone and index the code, then ask natural language questions about it.

## Tech Stack

- **Python** — Flask backend
- **LangChain** (LCEL) — RAG pipeline with conversation history
- **OpenAI** — `gpt-4o-mini` for chat, `text-embedding-3-small` for embeddings
- **ChromaDB** — local vector store for code chunks
- **GitPython** — repo cloning

---

## How to Run

### Step 1 — Clone the repository

```bash
git clone <repo-url>
cd End-to-end-Source-Code-Analysis-Generative-AI
```

### Step 2 — Create and activate a conda environment

```bash
conda create -n codeanalysis python=3.10 -y
conda activate codeanalysis
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Set up environment variables

Create a `.env` file in the project root:

```ini
OPENAI_API_KEY=your_openai_api_key_here
```

### Step 5 — Run the app

```bash
python app.py
```

Open [http://localhost:8080](http://localhost:8080) in your browser.

---

## Usage

1. Paste a public GitHub repository URL into the input field and click **Load Repo**
2. Wait for the repo to be cloned and indexed (may take 30–60 seconds)
3. Ask questions about the code in the chat:
   - *"What does this repository do?"*
   - *"Explain the main entry point"*
   - *"How is the database connection handled?"*
   - *"What functions are defined in helper.py?"*
   - *"How is authentication implemented?"*
4. Type **clear** to remove the loaded repository and start fresh

---

## Project Structure

```
├── app.py              # Flask app with LCEL RAG chain
├── store_index.py      # Indexes cloned repo into ChromaDB
├── src/
│   └── helper.py       # Repo cloning, loading, splitting, embeddings
├── templates/
│   └── index.html      # Frontend UI
├── static/
│   └── style.css       # GitHub-themed dark UI
├── requirements.txt
└── .env                # (not committed) API keys
```
