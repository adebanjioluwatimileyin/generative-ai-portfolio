from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import TokenTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import FAISS
import os
from dotenv import load_dotenv
from src.prompt import *


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


def file_processing(file_path):
    loader = PyPDFLoader(file_path)
    data = loader.load()

    question_gen = ''
    for page in data:
        question_gen += page.page_content

    splitter_ques_gen = TokenTextSplitter(
        model_name='gpt-4o-mini',
        chunk_size=10000,
        chunk_overlap=200
    )
    chunks_ques_gen = splitter_ques_gen.split_text(question_gen)
    document_ques_gen = [Document(page_content=t) for t in chunks_ques_gen]

    splitter_ans_gen = TokenTextSplitter(
        model_name='gpt-4o-mini',
        chunk_size=1000,
        chunk_overlap=100
    )
    document_answer_gen = splitter_ans_gen.split_documents(document_ques_gen)

    return document_ques_gen, document_answer_gen


def llm_pipeline(file_path):
    document_ques_gen, document_answer_gen = file_processing(file_path)

    llm_ques_gen = ChatOpenAI(temperature=0.3, model="gpt-4o-mini")

    PROMPT_QUESTIONS = PromptTemplate(template=prompt_template, input_variables=["text"])
    REFINE_PROMPT_QUESTIONS = PromptTemplate(
        input_variables=["existing_answer", "text"],
        template=refine_template,
    )

    # Refine chain implemented manually using LCEL
    initial_chain = PROMPT_QUESTIONS | llm_ques_gen | StrOutputParser()
    refine_chain = REFINE_PROMPT_QUESTIONS | llm_ques_gen | StrOutputParser()

    ques = initial_chain.invoke({"text": document_ques_gen[0].page_content})
    for doc in document_ques_gen[1:]:
        ques = refine_chain.invoke({"existing_answer": ques, "text": doc.page_content})

    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(document_answer_gen, embeddings)

    llm_answer_gen = ChatOpenAI(temperature=0.1, model="gpt-4o-mini")

    ques_list = ques.split("\n")
    filtered_ques_list = [
        element for element in ques_list
        if element.endswith('?') or element.endswith('.')
    ]

    qa_prompt = ChatPromptTemplate.from_template(
        "Answer the question based on the context below.\n\nContext: {context}\n\nQuestion: {question}"
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    answer_generation_chain = (
        {"context": vector_store.as_retriever() | format_docs, "question": RunnablePassthrough()}
        | qa_prompt
        | llm_answer_gen
        | StrOutputParser()
    )

    return answer_generation_chain, filtered_ques_list
