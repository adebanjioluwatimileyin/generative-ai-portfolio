# End-to-End Medical Chatbot with Generative AI

A RAG-based medical chatbot built with Flask, LangChain, Pinecone, and OpenAI. It answers medical questions by retrieving relevant context from a medical PDF book and generating accurate, concise responses using GPT-4o-mini.

## How It Works

```
Medical PDF → Chunk & Embed (MiniLM-L6-v2) → Pinecone vector store
                                                        ↓
User question → Retrieve top-3 chunks → GPT-4o-mini answers using context
```

## Features

- RAG pipeline over a medical reference book
- Sentence-transformers embeddings (384-dim, no API cost)
- Pinecone serverless vector store
- Flask web chat interface
- GPT-4o-mini for fast, accurate answers

## Setup

### 1. Navigate to the project directory

```bash
cd "/Users/adebanjiadelowo/Documents/GenerativeAIProjects/End to End Projects/End-to-end-Medical-Chatbot-Generative-AI"
```

### 2. Create and activate a conda environment

```bash
conda create -n medibot python=3.11 -y
conda activate medibot
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```ini
PINECONE_API_KEY=your-pinecone-api-key
OPENAI_API_KEY=your-openai-api-key
```

### 5. Create a Pinecone index (first time only)

Log in to [pinecone.io](https://pinecone.io) and create an index with:
- **Name:** `medicalbot`
- **Dimensions:** `384`
- **Metric:** `cosine`
- **Cloud:** AWS `us-east-1`

Then run the indexing script to embed and upload the PDF:

```bash
python store_index.py
```

> This only needs to run once. The embeddings are stored permanently in Pinecone.

### 6. Run the app

```bash
python app.py
```

Opens at `http://localhost:8080`.

## Tech Stack

- [Flask](https://flask.palletsprojects.com/) — web framework
- [LangChain](https://langchain.com/) — RAG pipeline (LCEL)
- [Pinecone](https://pinecone.io/) — vector store
- [OpenAI GPT-4o-mini](https://openai.com/) — language model
- [Sentence Transformers](https://www.sbert.net/) — embeddings (`all-MiniLM-L6-v2`)
