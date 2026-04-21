# Telegram Chatbot

A Telegram bot powered by GPT-4o-mini that maintains per-user conversation history for contextual multi-turn conversations.

## How It Works

```
User sends message → Bot retrieves conversation history → GPT-4o-mini generates reply → Bot responds
```

## Features

- Multi-turn conversation with full chat history per user
- `/clear` command to reset conversation context
- Lightweight and async using aiogram 3.x

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create a Telegram bot

1. Open Telegram and search for **@BotFather**
2. Send `/newbot` and follow the instructions
3. Copy the bot token provided

### 3. Set up environment variables

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your-openai-api-key
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
```

### 4. Run the bot

```bash
python main.py
```

## Commands

| Command | Description |
|---|---|
| `/start` | Start the conversation |
| `/help` | Show available commands |
| `/clear` | Clear conversation history |
| Any message | Get a GPT-4o-mini response |

## Tech Stack

- [aiogram 3.x](https://docs.aiogram.dev/) — Telegram bot framework
- [OpenAI GPT-4o-mini](https://openai.com/api/) — language model
- [python-dotenv](https://pypi.org/project/python-dotenv/) — environment variables
