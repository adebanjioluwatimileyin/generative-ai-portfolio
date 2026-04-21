import chainlit as cl
from src.llm import ask_order
from src.prompt import system_instruction


@cl.on_chat_start
async def start():
    cl.user_session.set("messages", [{"role": "system", "content": system_instruction}])
    await cl.Message(content="👋 Welcome to **Zomato OrderBot**! How can I help you today?").send()


@cl.on_message
async def main(message: cl.Message):
    messages = cl.user_session.get("messages")
    messages.append({"role": "user", "content": message.content})

    response = ask_order(messages)
    messages.append({"role": "assistant", "content": response})

    cl.user_session.set("messages", messages)
    await cl.Message(content=response).send()
