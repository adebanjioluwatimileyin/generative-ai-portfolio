import streamlit as st
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from dotenv import load_dotenv

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="transformers")

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="RAG Chatbot", page_icon="🤖", layout="wide")

st.markdown("""
    <style>
        .main { background-color: #0f1117; }
        .stChatMessage { border-radius: 12px; margin-bottom: 8px; }
        .stChatInputContainer { border-top: 1px solid #2d2d2d; padding-top: 10px; }
        .source-box {
            background: #1e1e2e;
            border-left: 3px solid #7c3aed;
            border-radius: 6px;
            padding: 10px 14px;
            font-size: 0.82rem;
            color: #aaa;
            margin-top: 6px;
        }
        .status-badge {
            display: inline-block;
            padding: 2px 10px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ Configuration")
    st.divider()

    urls_input = st.text_area(
        "Website URLs (one per line)",
        value="\n".join([
            "https://www.victoriaonmove.com.au/local-removalists.html",
            "https://victoriaonmove.com.au/index.html",
            "https://victoriaonmove.com.au/contact.html"
        ]),
        height=120
    )
    chunk_size = st.slider("Chunk size", 500, 2000, 1000, 100)
    top_k = st.slider("Top K results", 2, 10, 6)
    temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.1)

    load_btn = st.button("🔄 Load & Index URLs", use_container_width=True)

    st.divider()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.caption("Powered by LangChain + OpenAI + ChromaDB")

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None
if "indexed" not in st.session_state:
    st.session_state.indexed = False

# ── Main area ─────────────────────────────────────────────────────────────────
st.title("🤖 RAG Chatbot")
st.caption("Ask questions about the loaded website content")

# ── Load & index ──────────────────────────────────────────────────────────────
if load_btn:
    urls = [u.strip() for u in urls_input.strip().splitlines() if u.strip()]
    if not urls:
        st.sidebar.error("Please enter at least one URL.")
    else:
        with st.spinner("Loading and indexing content..."):
            try:
                loader = UnstructuredURLLoader(urls=urls)
                data = loader.load()

                splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=100)
                docs = splitter.split_documents(data)

                vectorstore = Chroma.from_documents(
                    documents=docs,
                    embedding=OpenAIEmbeddings()
                )
                retriever = vectorstore.as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": top_k}
                )

                llm = ChatOpenAI(model="gpt-4o-mini", temperature=temperature)

                system_prompt = (
                    "You are a helpful assistant. Use the retrieved context below to answer "
                    "the question accurately and concisely. If you don't know the answer, say so.\n\n"
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
                st.sidebar.success(f"✅ Indexed {len(docs)} chunks from {len(urls)} URL(s)")
            except Exception as e:
                st.sidebar.error(f"Error: {e}")

# ── Chat status ───────────────────────────────────────────────────────────────
if not st.session_state.indexed:
    st.info("👈 Enter URLs in the sidebar and click **Load & Index URLs** to get started.")

# ── Chat history ──────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("📄 Sources", expanded=False):
                for src in msg["sources"]:
                    st.markdown(f'<div class="source-box">{src}</div>', unsafe_allow_html=True)

# ── Chat input ────────────────────────────────────────────────────────────────
if query := st.chat_input("Ask a question about the website...", disabled=not st.session_state.indexed):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.rag_chain.invoke({"input": query})
            answer = response["answer"]
            sources = list({doc.metadata.get("source", "Unknown") for doc in response.get("context", [])})

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
