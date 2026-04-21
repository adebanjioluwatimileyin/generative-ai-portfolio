# Generative AI Projects

A collection of end-to-end Generative AI projects covering RAG pipelines, LLM fine-tuning, chatbots, vector databases, and LLMOps — built with LangChain, OpenAI, Google Vertex AI, Amazon Bedrock, and more.

---

## End-to-End-Projects

| Project | Description | Stack |
|---|---|---|
| [Medical Chatbot](End-to-End-Projects/End-to-end-Medical-Chatbot-Generative-AI/) | RAG-based chatbot that answers medical questions from a PDF knowledge base | OpenAI, Pinecone, LangChain, Flask |
| [Source Code Analyser](End-to-End-Projects/End-to-end-Source-Code-Analysis-Generative-AI/) | Clone any GitHub repo and ask natural language questions about the code | OpenAI, ChromaDB, LangChain, Flask |
| [Zomato OrderBot](End-to-End-Projects/LLM-Apps-with-Chainlit/) | Conversational food ordering chatbot with a full menu | OpenAI, Chainlit |

---

## LLMOps

| Project | Description | Stack |
|---|---|---|
| [RAG with Amazon Bedrock](LLMOps/End-to-end-RAG-using-Amazon-Bedrock/) | RAG pipeline over PDF documents using AWS Bedrock and Titan embeddings | Bedrock, ChromaDB, LangChain, Streamlit |
| [Bedrock Generative AI](LLMOps/GenerativeAI-Project-Bedrock/) | Document Q&A with FAISS vector store on AWS Bedrock | Bedrock, FAISS, LangChain, Streamlit |
| [LLM-Powered Chatbot](LLMOps/LLM-Powered-Chatbot/) | Conversational chatbot powered by Gemini 1.5 Flash on Google Cloud | Vertex AI, Gemini 1.5 Flash, Flask |
| [VertexAI Local Demo](LLMOps/VertexAI-Local-Demo/) | Local Vertex AI integration demo | Vertex AI |
| [RAG on Vertex AI](LLMOps/RAG%20on%20VertexAI.ipynb) | RAG pipeline notebook using Vertex AI embeddings and Gemini | Vertex AI, LangChain |
| [Vertex AI Demo](LLMOps/vertexai%20demo.ipynb) | Multimodal demos with Gemini 1.5 Flash (text, image, chat) | Vertex AI, Gemini 1.5 Flash |
| [Vertex AI Fine-Tuning](LLMOps/vertexai_llm_fine_tuning_supervised.ipynb) | Supervised fine-tuning of Gemini 1.5 Flash on BBC News summaries | Vertex AI SFT, Gemini 1.5 Flash |

---

## RAG (Retrieval Augmented Generation)

| Project | Description | Stack |
|---|---|---|
| [RAG Demo](RAG/RAG-Demo/) | Basic RAG pipeline demonstration | LangChain, OpenAI |
| [RAG with Gemini](RAG/RAG-gemini/) | PDF-based RAG chatbot with Gemini and ChromaDB | Gemini, ChromaDB, LangChain, Streamlit |

---

## OpenAI

| Project | Description | Stack |
|---|---|---|
| [OpenAI Demo](OpenAI/OpenAI-Demo/) | OpenAI API demos and experiments | OpenAI |
| [DALL-E Demo](OpenAI/DALLE-demo/) | Image generation with DALL-E | OpenAI DALL-E |
| [Audio Translation](OpenAI/Audio-Translation/) | Speech-to-text using Whisper API | OpenAI Whisper |
| [Telegram Chatbot](OpenAI/Telegram-chatbot/) | Chatbot integrated with Telegram | OpenAI, Telegram Bot API |
| [Fine-Tuned Classification](OpenAI/Fine_tuned_classification.ipynb) | Text classification using a fine-tuned OpenAI model | OpenAI Fine-tuning |

---

## LangChain

| Project | Description | Stack |
|---|---|---|
| [LangChain Projects](LangChain/LangChain-Projects/) | Custom chatbots, agents, multi-dataframe agents, and Hugging Face integrations | LangChain, OpenAI, HuggingFace |

---

## Master-Vector-Database

| Project | Description | Stack |
|---|---|---|
| [Vector Database Demos](Master-Vector-Database/Vector-Database-Demos/) | ChromaDB, Pinecone, and Weaviate demos with LangChain | ChromaDB, Pinecone, Weaviate |

---

## Fine-Tuning-LLMs

| Project | Description | Stack |
|---|---|---|
| [Llama 2 Fine-Tuning](Fine-Tuning-LLMs/Llama2-Fine-Tuning/) | Fine-tuning Llama 2 with custom datasets | Llama 2, HuggingFace |

---

## Open-Source-LLMs

| Project | Description | Stack |
|---|---|---|
| [Falcon 7B Demos](Open-Source-LLMs/Falcon-7B-Demos/) | Falcon 7B with ChromaDB multi-doc retriever and LangChain | Falcon 7B, ChromaDB, LangChain |
| [Llama 2 Demos](Open-Source-LLMs/Llama2-Demos/) | Running Llama 2 locally, LangChain integration, website bot | Llama 2, Pinecone, LangChain |

---

## Other Topics

- **[Data-Preprocessing-and-Embeddings](Data-Preprocessing-and-Embeddings/)** — text preprocessing, word embeddings, and ML classification
- **[HuggingFace-and-API](HuggingFace-and-API/)** — model inference, pipelines, text summarization, and text-to-speech
- **[LlamaIndex](LlamaIndex/)** — document indexing and querying with LlamaIndex

---

## Setup

Most projects use conda environments. Each project folder has its own `requirements.txt` and `README.md` with specific setup instructions.

```bash
conda create -n <env-name> python=3.10 -y
conda activate <env-name>
pip install -r requirements.txt
```

You will need API keys depending on the project:
- `OPENAI_API_KEY` — OpenAI projects
- `PINECONE_API_KEY` — Pinecone vector store projects
- AWS credentials — Amazon Bedrock projects
- Google Cloud credentials — Vertex AI projects
