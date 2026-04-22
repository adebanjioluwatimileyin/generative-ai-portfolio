# End-to-End Generative AI with Amazon Bedrock

A Retrieval Augmented Generation (RAG) chatbot built with Streamlit, LangChain, and Amazon Bedrock. Load PDF documents into a FAISS vector store and ask questions answered using Llama 3 70B via Bedrock. Also includes a standalone multilingual chatbot demo.

## How It Works

```
PDF files → Load & split → FAISS index (persisted to disk)
                                    ↓
User question → Retrieve top-5 chunks → Llama 3 70B (Bedrock) answers using context
```

## Features

- Load and index all PDFs from the `pdf-data/` folder
- Persistent FAISS vector store (survives restarts)
- Streaming responses for real-time output
- Source citations — see which page of which PDF each answer came from
- FAISS index status indicator in sidebar
- Chat input disabled until index is built
- Chat history with session state
- Titan Embed v1 embeddings via Amazon Bedrock
- Llama 3 70B Chat via Amazon Bedrock (Converse API)
- Standalone multilingual chatbot demo (`research/bedrock_trials.py`)

## Setup

### 1. Create and activate a conda environment

```bash
conda create -n bedrockproj python=3.11 -y
conda activate bedrockproj
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

To get your credentials: **AWS Console → IAM → Users → your user → Security credentials → Create access key**.

### 4. Bedrock model access

Bedrock foundation models are **automatically enabled** when first invoked — no manual activation needed.

Models used in this project:
- `amazon.titan-embed-text-v1` (embeddings)
- `meta.llama3-70b-instruct-v1:0` (generation)

> **Note:** Account admins can restrict model access via IAM policies and Service Control Policies if needed.

### 5. Add PDFs and run

Place your PDF files in the `pdf-data/` folder, then:

```bash
streamlit run main.py
```

Opens at `http://localhost:8501`.

## Usage

1. Click **Build Vector Store** in the sidebar to index PDFs
2. Ask questions in the chat input

## Chatbot Demo

A simpler multilingual chatbot (no RAG) using AI21 Jurassic-2:

```bash
streamlit run research/bedrock_trials.py
```

## Tech Stack

- [Streamlit](https://streamlit.io/) — frontend
- [LangChain](https://langchain.com/) — RAG pipeline
- [Amazon Bedrock](https://aws.amazon.com/bedrock/) — embeddings (Titan) and generation (Llama 3 70B)
- [FAISS](https://faiss.ai/) — vector store
