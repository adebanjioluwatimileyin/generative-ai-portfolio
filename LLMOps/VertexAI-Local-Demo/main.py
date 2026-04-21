import vertexai
import streamlit as st
import os
from vertexai.generative_models import GenerativeModel, GenerationConfig
from dotenv import load_dotenv

load_dotenv()

project_id = os.getenv("project_id")
project_region = os.getenv("region", "us-central1")

vertexai.init(project=project_id, location=project_region)

model = GenerativeModel("gemini-1.5-flash")


def user_interfaces():
    st.set_page_config(page_title="VertexAI Local Demo")
    st.header("Vertex AI Local Demo")
    st.caption("Powered by Gemini 1.5 Flash")

    user_question = st.text_input("Ask me anything...")

    if user_question:
        with st.spinner("Thinking..."):
            response = model.generate_content(user_question)
            st.write(response.text)


if __name__ == "__main__":
    user_interfaces()
