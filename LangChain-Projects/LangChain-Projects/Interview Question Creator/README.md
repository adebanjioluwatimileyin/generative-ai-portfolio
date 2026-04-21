# Interview Question Creator

An AI-powered tool that generates interview and exam questions from any PDF document. Upload a PDF, and the app extracts key concepts and produces a downloadable CSV of questions and answers.

## Tech Stack

- **Python** — application logic
- **FastAPI** — async web backend
- **LangChain** — LLM pipeline with refine chain for question generation
- **OpenAI** — GPT model for question and answer generation
- **Jinja2** — HTML templating

---

## How to Run

### Step 1 — Create and activate a conda environment

```bash
conda create -n interview python=3.10 -y
conda activate interview
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

### Step 4 — Run the app

```bash
python app.py
```

Open [http://localhost:8080](http://localhost:8080) in your browser.

---

## Usage

1. Upload a PDF document (lecture notes, textbook chapter, documentation, etc.)
2. Click **Analyze** to generate questions
3. The app processes the document and produces a `QA.csv` file with questions and answers
4. Download the CSV for study or interview prep

## How It Works

- The PDF is split into chunks and passed through a LangChain **refine chain**
- A first pass generates an initial set of questions from each chunk
- Subsequent passes refine and deduplicate questions using additional context
- Answers are generated for each question and saved to `static/output/QA.csv`
