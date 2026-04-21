from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from src.helper import repo_ingestion
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__)

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

embeddings = OpenAIEmbeddings(disallowed_special=())
persist_directory = "db"

vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
retriever = vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 8})

llm = ChatOpenAI(model="gpt-4o-mini")

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert code analyst. Use the retrieved code context to answer questions about the repository.
Be specific, reference file names and function names when relevant.

Context:
{context}"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}"),
])

store: dict[str, BaseChatMessageHistory] = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


def format_docs(docs):
    return "\n\n".join(f"# {doc.metadata.get('source', 'unknown')}\n{doc.page_content}" for doc in docs)


rag_chain = (
    RunnablePassthrough.assign(context=lambda x: format_docs(retriever.invoke(x["question"])))
    | prompt
    | llm
    | StrOutputParser()
)

chain_with_history = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="chat_history",
)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/chatbot", methods=["POST"])
def gitRepo():
    user_input = request.form.get("question", "").strip()
    if not user_input:
        return jsonify({"error": "No URL provided"}), 400

    try:
        repo_ingestion(user_input)
        os.system("python store_index.py")
        global vectordb, retriever
        vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
        retriever = vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 8})
        return jsonify({"response": "Repository loaded successfully."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get", methods=["POST"])
def chat():
    msg = request.form.get("msg", "").strip()
    if not msg:
        return "Please enter a message.", 400

    if msg.lower() == "clear":
        os.system("rm -rf repo")
        store.clear()
        return "Repository cleared."

    try:
        result = chain_with_history.invoke(
            {"question": msg},
            config={"configurable": {"session_id": "default"}},
        )
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
