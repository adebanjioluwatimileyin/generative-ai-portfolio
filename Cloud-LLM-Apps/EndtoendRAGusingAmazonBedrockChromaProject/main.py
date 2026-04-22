import os
import boto3
import streamlit as st
from langchain_aws import ChatBedrock, BedrockEmbeddings
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

aws_access_key_id = os.getenv("aws_access_key_id")
aws_secret_access_key = os.getenv("aws_secret_access_key")
region_name = os.getenv("region_name")

PROMPT_TEMPLATE = """You are a helpful assistant that answers questions strictly based on the provided context.

Guidelines:
- Answer only from the context below. Do not use outside knowledge.
- If the answer is not in the context, say "I couldn't find that information in the documents."
- Be clear, well-structured, and thorough in your response.
- Where relevant, reference which part of the document supports your answer.

Context:
{context}

Question: {question}

Answer:"""

bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name=region_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)

bedrock_embeddings = BedrockEmbeddings(
    model_id="amazon.titan-embed-text-v1",
    client=bedrock
)

PROMPT = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)


def get_documents():
    loader = PyPDFDirectoryLoader("data")
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_documents(documents)


def get_vector_store(docs):
    Chroma.from_documents(
        docs,
        embedding=bedrock_embeddings,
        persist_directory="./db"
    )


def get_llm():
    return ChatBedrock(
        model_id="mistral.mistral-7b-instruct-v0:2",
        client=bedrock,
        model_kwargs={"max_tokens": 2048}
    )


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def get_retriever(vectorstore):
    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )


def get_llm_response_stream(llm, vectorstore, query):
    chain = (
        {"context": get_retriever(vectorstore) | format_docs, "question": RunnablePassthrough()}
        | PROMPT | llm | StrOutputParser()
    )
    return chain.stream(query)


def get_sources(vectorstore, query):
    return get_retriever(vectorstore).invoke(query)


def db_exists():
    return os.path.exists("./db/chroma.sqlite3")


def main():
    st.set_page_config(page_title="RAG with Amazon Bedrock", page_icon="📄", layout="wide")

    st.markdown("""
        <style>
            [data-testid="stSidebar"] { background-color: #1a1d2e; }
            .stChatMessage { border-radius: 12px; margin-bottom: 8px; }
        </style>
    """, unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.sidebar:
        st.title("⚙️ Configuration")
        st.divider()

        if db_exists():
            st.success("Vector store ready", icon="✅")
        else:
            st.warning("No vector store — build one first", icon="⚠️")

        st.markdown("Place PDF files in the **`data/`** folder, then click **Build Vector Store**.")

        if st.button("🔄 Build Vector Store", use_container_width=True):
            with st.spinner("Loading and indexing PDFs..."):
                docs = get_documents()
                if not docs:
                    st.error("No PDFs found in the `data/` folder.")
                else:
                    get_vector_store(docs)
                    sources = set(d.metadata.get("source", "") for d in docs)
                    st.success(f"Indexed {len(docs)} chunks from {len(sources)} PDF(s)")
                    st.rerun()

        st.divider()
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        st.caption("Powered by LangChain + Amazon Bedrock + ChromaDB")

    st.title("📄 RAG with Amazon Bedrock")
    st.caption("Ask questions about your PDF documents")

    if not db_exists():
        st.info("Build the vector store first using the sidebar before asking questions.", icon="ℹ️")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and msg.get("sources"):
                with st.expander("📚 View sources"):
                    for doc in msg["sources"]:
                        src = doc.metadata.get("source", "Unknown")
                        page = doc.metadata.get("page", "?")
                        st.markdown(f"**{os.path.basename(src)}** — page {page + 1}")
                        st.caption(doc.page_content[:300] + "…")

    if query := st.chat_input("Ask a question about the documents...", disabled=not db_exists()):
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        sources = []
        with st.chat_message("assistant"):
            try:
                vectordb = Chroma(persist_directory="./db", embedding_function=bedrock_embeddings)
                llm = get_llm()
                sources = get_sources(vectordb, query)
                answer = st.write_stream(get_llm_response_stream(llm, vectordb, query))
            except Exception as e:
                answer = f"Something went wrong: {e}"
                st.error(answer)

            if sources:
                with st.expander("📚 View sources"):
                    for doc in sources:
                        src = doc.metadata.get("source", "Unknown")
                        page = doc.metadata.get("page", "?")
                        st.markdown(f"**{os.path.basename(src)}** — page {page + 1}")
                        st.caption(doc.page_content[:300] + "…")

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": sources
        })


if __name__ == "__main__":
    main()
