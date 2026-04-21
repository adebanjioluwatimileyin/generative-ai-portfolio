# RAG Chatbot (Gemini)

A Retrieval Augmented Generation (RAG) chatbot built with Streamlit, LangChain, and Google Gemini. Upload a PDF, index its content into a vector store, and ask questions answered using retrieved context.

## How It Works

```
Upload PDF → Split into chunks → ChromaDB (vector store)
                                        ↓
User question → Retrieve relevant chunks → Gemini Pro answers using context
```

## Features

- Upload any PDF and index it into ChromaDB
- Configurable chunk size, top-K retrieval, and temperature
- Persistent chat history with page-level source citations
- Dark themed Streamlit UI with sidebar controls

## Setup

### 1. Create and activate a conda environment

```bash
conda create -n rag-gemini python=3.11 -y
conda activate rag-gemini
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the project root:

```
GOOGLE_API_KEY=your-google-api-key
```

Get a key at: https://ai.google.dev/gemini-api/docs/api-key

### 4. Run the app

```bash
streamlit run app.py
```

Opens at `http://localhost:8501`.

## Usage

1. Upload a PDF in the sidebar
2. Click **Load & Index PDF**
3. Ask questions in the chat input

## Tech Stack

- [Streamlit](https://streamlit.io/) — frontend
- [LangChain](https://langchain.com/) — RAG pipeline
- [ChromaDB](https://www.trychroma.com/) — vector store
- [Google Gemini](https://ai.google.dev/) — embeddings and generation
