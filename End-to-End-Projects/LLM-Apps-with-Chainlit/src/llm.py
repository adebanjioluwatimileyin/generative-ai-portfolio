from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def ask_order(messages: list, model: str = "gpt-4o-mini", temperature: float = 0) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content
