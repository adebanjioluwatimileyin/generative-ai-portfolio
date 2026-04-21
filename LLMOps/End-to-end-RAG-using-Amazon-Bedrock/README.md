# End-to-End RAG with Amazon Bedrock

A Retrieval Augmented Generation (RAG) chatbot built with Streamlit, LangChain, and Amazon Bedrock. Load PDF documents into a ChromaDB vector store and ask questions answered using Mistral 7B via Bedrock.

## How It Works

```
PDF files → Load & split → ChromaDB (vector store, persisted to disk)
                                    ↓
User question → Retrieve top-3 chunks → Mistral 7B (Bedrock) answers using context
```

## Features

- Load and index all PDFs from the `data/` folder
- Persistent ChromaDB vector store (survives restarts)
- Chat history with session state
- Titan Embed v1 embeddings via Amazon Bedrock
- Mistral 7B Instruct via Amazon Bedrock

## Setup

### 1. Create and activate a conda environment

```bash
conda create -n bedrock-rag python=3.11 -y
conda activate bedrock-rag
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the project root:

```
aws_access_key_id=your-aws-access-key-id
aws_secret_access_key=your-aws-secret-access-key
region_name=us-east-1
```

### 4. Enable Bedrock model access

In the AWS Console, go to **Amazon Bedrock → Model access** and enable:
- `amazon.titan-embed-text-v1` (embeddings)
- `mistral.mistral-7b-instruct-v0:2` (generation)

### 5. Add PDFs and run

Place your PDF files in the `data/` folder, then:

```bash
streamlit run main.py
```

Opens at `http://localhost:8501`.

## Usage

1. Click **Build Vector Store** in the sidebar to index PDFs
2. Ask questions in the chat input

## Tech Stack

- [Streamlit](https://streamlit.io/) — frontend
- [LangChain](https://langchain.com/) — RAG pipeline
- [Amazon Bedrock](https://aws.amazon.com/bedrock/) — embeddings (Titan) and generation (Mistral 7B)
- [ChromaDB](https://www.trychroma.com/) — vector store
