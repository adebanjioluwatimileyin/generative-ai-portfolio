import vertexai
import streamlit as st
import os
from vertexai.generative_models import GenerativeModel, GenerationConfig
from dotenv import load_dotenv

load_dotenv()

project_id = os.getenv("project_id")
project_region = os.getenv("region", "us-central1")

vertexai.init(project=project_id, location=project_region)

SYSTEM_INSTRUCTION = """You are a helpful, knowledgeable, and friendly AI assistant powered by Google Gemini.
- Be concise but thorough.
- Use markdown formatting when it improves readability (code blocks, lists, bold text).
- If you don't know something, say so honestly.
- Keep a conversational, approachable tone."""

model = GenerativeModel(
    "gemini-2.0-flash",
    system_instruction=SYSTEM_INSTRUCTION,
    generation_config=GenerationConfig(
        temperature=0.7,
        max_output_tokens=2048,
    )
)


def get_chat_session():
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat()
    return st.session_state.chat_session


def stream_response(query):
    chat = get_chat_session()
    for chunk in chat.send_message_streaming(query):
        yield chunk.text


def main():
    st.set_page_config(page_title="Gemini Chatbot", page_icon="✨", layout="wide")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.sidebar:
        st.title("⚙️ Configuration")
        st.divider()
        st.markdown("**Model:** Gemini 2.0 Flash")
        st.markdown("**Provider:** Google Vertex AI")
        st.divider()

        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            del st.session_state.chat_session
            st.rerun()

        st.caption("Powered by Vertex AI + Streamlit")

    st.title("✨ Gemini 2.0 Flash Chatbot")
    st.caption("Ask me anything — I remember the full conversation.")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if query := st.chat_input("Type your message..."):
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        with st.chat_message("assistant"):
            try:
                answer = st.write_stream(stream_response(query))
            except Exception as e:
                answer = f"Something went wrong: {e}"
                st.error(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    main()
