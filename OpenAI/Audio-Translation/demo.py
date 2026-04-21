import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

audio_file = open("Recording.mp3", "rb")
output = client.audio.translations.create(
    model="whisper-1",
    file=audio_file
)
print(output.text)
