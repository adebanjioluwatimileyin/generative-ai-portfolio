import boto3
import streamlit as st
from langchain_aws import BedrockLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Bedrock client
bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

model_id = "ai21.j2-mid-v1"

llm = BedrockLLM(
    model_id=model_id,
    client=bedrock_client,
    model_kwargs={"temperature": 0.9}
)


def my_chatbot(language, user_text):
    prompt = PromptTemplate(
        input_variables=["language", "user_text"],
        template="You are a chatbot. You are in {language}.\n\n{user_text}"
    )
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"language": language, "user_text": user_text})


st.title("Bedrock Chatbot")

language = st.sidebar.selectbox("Language", ["english", "spanish", "hindi"])

if language:
    user_text = st.sidebar.text_area(label="What is your question?", max_chars=100)

if user_text:
    response = my_chatbot(language, user_text)
    st.write(response)
