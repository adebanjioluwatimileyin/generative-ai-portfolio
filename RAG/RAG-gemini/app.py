import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from dotenv import load_dotenv
import tempfile
import os

load_dotenv()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="RAG Chatbot (Gemini)", page_icon="🔮", layout="wide")

st.markdown("""
    <style>
        .main { background-color: #0f1117; }
        .stChatMessage { border-radius: 12px; margin-bottom: 8px; }
        .stChatInputContainer { border-top: 1px solid #2d2d2d; padding-top: 10px; }
        .source-box {
            background: #1e1e2e;
            border-left: 3px solid #4285f4;
            border-radius: 6px;
            padding: 10px 14px;
            font-size: 0.82rem;
            color: #aaa;
            margin-top: 6px;
        }
    </style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ Configuration")
    st.divider()

    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
    chunk_size = st.slider("Chunk size", 500, 2000, 1000, 100)
    top_k = st.slider("Top K results", 2, 10, 10)
    temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.1)

    load_btn = st.button("🔄 Load & Index PDF", use_container_width=True)

    st.divider()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.caption("Powered by LangChain + Gemini + ChromaDB")

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None
if "indexed" not in st.session_state:
    st.session_state.indexed = False

# ── Main area ─────────────────────────────────────────────────────────────────
st.title("🔮 RAG Chatbot (Gemini)")
st.caption("Upload a PDF and ask questions about its content")

# ── Load & index ──────────────────────────────────────────────────────────────
if load_btn:
    if uploaded_file is None:
        st.sidebar.error("Please upload a PDF file.")
    else:
        with st.spinner("Loading and indexing PDF..."):
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name

                loader = PyPDFLoader(tmp_path)
                data = loader.load()
                os.unlink(tmp_path)

                splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=100)
                docs = splitter.split_documents(data)

                vectorstore = Chroma.from_documents(
                    documents=docs,
                    embedding=GoogleGenerativeAIEmbeddings(model="models/embedding-001")
                )
                retriever = vectorstore.as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": top_k}
                )

                llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=temperature, max_tokens=None)

                system_prompt = (
                    "You are an assistant for question-answering tasks. "
                    "Use the following pieces of retrieved context to answer "
                    "the question accurately and concisely. "
                    "If you don't know the answer, say so.\n\n"
                    "{context}"
                )
                prompt = ChatPromptTemplate.from_messages([
                    ("system", system_prompt),
                    ("human", "{input}"),
                ])

                def format_docs(docs):
                    return "\n\n".join(doc.page_content for doc in docs)

                st.session_state.rag_chain = RunnableParallel({
                    "context": retriever,
                    "input": RunnablePassthrough()
                }).assign(
                    answer=(
                        lambda x: {"context": format_docs(x["context"]), "input": x["input"]}
                    ) | prompt | llm | StrOutputParser()
                )
                st.session_state.indexed = True
                st.session_state.messages = []
                st.sidebar.success(f"✅ Indexed {len(docs)} chunks from {uploaded_file.name}")
            except Exception as e:
                st.sidebar.error(f"Error: {e}")

# ── Chat status ───────────────────────────────────────────────────────────────
if not st.session_state.indexed:
    st.info("👈 Upload a PDF in the sidebar and click **Load & Index PDF** to get started.")

# ── Chat history ──────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("📄 Sources", expanded=False):
                for src in msg["sources"]:
                    st.markdown(f'<div class="source-box">{src}</div>', unsafe_allow_html=True)

# ── Chat input ────────────────────────────────────────────────────────────────
if query := st.chat_input("Ask a question about the PDF...", disabled=not st.session_state.indexed):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.rag_chain.invoke({"input": query})
            answer = response["answer"]
            sources = list({
                f"Page {doc.metadata.get('page', '?') + 1} — {doc.metadata.get('source', 'Unknown')}"
                for doc in response.get("context", [])
            })

        st.markdown(answer)
        if sources:
            with st.expander("📄 Sources", expanded=False):
                for src in sources:
                    st.markdown(f'<div class="source-box">{src}</div>', unsafe_allow_html=True)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources
    })
