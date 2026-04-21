# RAG Chatbot Demo

A Retrieval Augmented Generation (RAG) chatbot built with Streamlit, LangChain, and OpenAI. It loads content from websites, indexes it into a vector store, and answers user questions using the retrieved context.

## How It Works

```
Website URLs → Load content → Split into chunks → ChromaDB (vector store)
                                                          ↓
User question → Retrieve relevant chunks → GPT-4o-mini answers using context
```

## Features

- Load and index content from multiple website URLs
- Configurable chunk size, top-K retrieval, and temperature
- Persistent chat history with source citations
- Dark themed Streamlit UI

## Setup

### 1. Create and activate a conda environment

```bash
conda create -n rag-demo python=3.11 -y
conda activate rag-demo
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your-openai-api-key
```

### 4. Run the app

```bash
streamlit run app.py
```

Opens at `http://localhost:8501`.

## Usage

1. Enter one or more website URLs in the sidebar (one per line)
2. Click **Load & Index URLs**
3. Ask questions in the chat input

## Tech Stack

- [Streamlit](https://streamlit.io/) — frontend
- [LangChain](https://langchain.com/) — RAG pipeline
- [ChromaDB](https://www.trychroma.com/) — vector store
- [OpenAI](https://openai.com/) — embeddings and GPT-4o-mini
