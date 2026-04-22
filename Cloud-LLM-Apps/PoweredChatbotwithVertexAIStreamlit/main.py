import streamlit as st
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

SYSTEM_INSTRUCTION = """You are a helpful, knowledgeable, and friendly AI assistant powered by Google Gemini.
- Be concise but thorough.
- Use markdown formatting when it improves readability (code blocks, lists, bold text).
- If you don't know something, say so honestly.
- Keep a conversational, approachable tone."""

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def get_chat_session():
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.7,
                max_output_tokens=2048,
            )
        )
    return st.session_state.chat_session


def stream_response(query):
    chat = get_chat_session()
    for chunk in chat.send_message_stream(query):
        yield chunk.text


def main():
    st.set_page_config(page_title="Gemini Chatbot", page_icon="✨", layout="wide")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.sidebar:
        st.title("⚙️ Configuration")
        st.divider()
        st.markdown("**Model:** Gemini 2.5 Flash")
        st.markdown("**Provider:** Google Gemini API")
        st.divider()

        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            if "chat_session" in st.session_state:
                del st.session_state.chat_session
            st.rerun()

        st.caption("Powered by Gemini API + Streamlit")

    st.title("✨ Gemini 2.5 Flash Chatbot")
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
