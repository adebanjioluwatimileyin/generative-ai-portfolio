import asyncio
import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from openai import OpenAI

load_dotenv()

logging.basicConfig(level=logging.INFO)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

model_name = "gpt-4o-mini"

# Store conversation history per user
conversation_history = {}

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def welcome(message: types.Message):
    await message.reply("Hi! I am Tele Bot powered by GPT-4o-mini. How can I assist you?")


@dp.message(Command("help"))
async def helper(message: types.Message):
    await message.reply(
        "Hi! I'm a Telegram chatbot. Here are the available commands:\n"
        "/start - Start the conversation\n"
        "/clear - Clear conversation history\n"
        "/help - Show this help menu"
    )


@dp.message(Command("clear"))
async def clear(message: types.Message):
    conversation_history[message.chat.id] = []
    await message.reply("Conversation history cleared.")


@dp.message()
async def chatgpt(message: types.Message):
    chat_id = message.chat.id

    if chat_id not in conversation_history:
        conversation_history[chat_id] = []

    conversation_history[chat_id].append({"role": "user", "content": message.text})

    print(f">>> USER: {message.text}")

    response = client.chat.completions.create(
        model=model_name,
        messages=conversation_history[chat_id]
    )

    reply = response.choices[0].message.content
    conversation_history[chat_id].append({"role": "assistant", "content": reply})

    print(f">>> BOT: {reply}")
    await message.reply(reply)


async def main():
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
