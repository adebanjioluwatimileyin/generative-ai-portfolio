# End-to-End Generative AI with Amazon Bedrock

A Retrieval Augmented Generation (RAG) chatbot built with Streamlit, LangChain, and Amazon Bedrock. Load PDF documents into a FAISS vector store and ask questions answered using Llama 2 70B via Bedrock. Also includes a standalone multilingual chatbot demo.

## How It Works

```
PDF files → Load & split → FAISS index (persisted to disk)
                                    ↓
User question → Retrieve top-3 chunks → Llama 2 70B (Bedrock) answers using context
```

## Features

- Load and index all PDFs from the `pdf-data/` folder
- Persistent FAISS vector store (survives restarts)
- Chat history with session state
- Titan Embed v1 embeddings via Amazon Bedrock
- Llama 2 70B Chat via Amazon Bedrock
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

### 3. Configure AWS credentials

Install the AWS CLI:
```bash
# macOS
brew install awscli

# or download from:
# https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
```

Then configure:
```bash
aws configure
```

Enter your `AWS Access Key ID`, `Secret Access Key`, and default region (`us-east-1`).

### 4. Enable Bedrock model access

In the AWS Console, go to **Amazon Bedrock → Model access** and enable:
- `amazon.titan-embed-text-v1` (embeddings)
- `meta.llama2-70b-chat-v1` (generation)
- `ai21.j2-mid-v1` (chatbot demo)

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
- [Amazon Bedrock](https://aws.amazon.com/bedrock/) — embeddings (Titan) and generation (Llama 2 70B)
- [FAISS](https://faiss.ai/) — vector store
