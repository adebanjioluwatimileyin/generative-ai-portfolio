import boto3
import streamlit as st
from langchain_aws import BedrockLLM, BedrockEmbeddings
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


PROMPT_TEMPLATE = """
Human: Use the following pieces of context to provide a
concise answer to the question at the end. Summarize with at least
250 words with detailed explanations. If you don't know the answer,
just say that you don't know - don't try to make up an answer.
<context>
{context}
</context>

Question: {question}
"""


# Bedrock client
bedrock = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

# Embeddings model
bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1", client=bedrock)

PROMPT = PromptTemplate(template=PROMPT_TEMPLATE, input_variables=["context", "question"])


def get_documents():
    loader = PyPDFDirectoryLoader("pdf-data")
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=500)
    return splitter.split_documents(documents)


def get_vector_store(docs):
    vectorstore = FAISS.from_documents(docs, bedrock_embeddings)
    vectorstore.save_local("faiss_index")


def get_llm():
    return BedrockLLM(
        model_id="meta.llama2-70b-chat-v1",
        client=bedrock,
        model_kwargs={"max_gen_len": 512}
    )


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def get_response_llm(llm, vectorstore_faiss, query):
    retriever = vectorstore_faiss.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | PROMPT | llm | StrOutputParser()
    )
    return chain.invoke(query)


def main():
    st.set_page_config(page_title="RAG with Amazon Bedrock", page_icon="🦙", layout="wide")

    st.markdown("""
        <style>
            .main { background-color: #0f1117; }
            .stChatMessage { border-radius: 12px; margin-bottom: 8px; }
        </style>
    """, unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.sidebar:
        st.title("⚙️ Configuration")
        st.divider()
        st.markdown("Place PDF files in the **`pdf-data/`** folder, then click **Build Vector Store**.")

        if st.button("🔄 Build Vector Store", use_container_width=True):
            with st.spinner("Loading and indexing PDFs..."):
                docs = get_documents()
                get_vector_store(docs)
                st.success(f"Indexed {len(docs)} chunks")

        st.divider()
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        st.caption("Powered by LangChain + Amazon Bedrock + FAISS")

    st.title("🦙 RAG with Amazon Bedrock")
    st.caption("Ask questions about your PDF documents")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if query := st.chat_input("Ask a question about the documents..."):
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                faiss_index = FAISS.load_local("faiss_index", bedrock_embeddings, allow_dangerous_deserialization=True)
                llm = get_llm()
                answer = get_response_llm(llm, faiss_index, query)
            st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    main()
