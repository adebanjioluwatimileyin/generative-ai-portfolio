# Audio Translator

A Flask web app that transcribes audio files and translates the content into any language using OpenAI's Whisper and GPT-4o-mini.

## How It Works

```
User uploads audio → Whisper transcribes to English → GPT-4o-mini translates → Result displayed
```

## Features

- Upload audio files (MP3, WAV, M4A, OGG)
- Transcribe speech to text using OpenAI Whisper
- Translate transcript into any language
- Dark themed responsive UI
- Returns both the original transcript and the translation

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up environment variables

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your-openai-api-key
```

### 3. Run the app

```bash
python app.py
```

Opens at `http://localhost:8080`.

## Usage

1. Click the upload area and select an audio file
2. Choose a target language from the dropdown (or type a custom one)
3. Click **Translate**
4. View the original transcript and translation

## Tech Stack

- [Flask](https://flask.palletsprojects.com/) — web framework
- [OpenAI Whisper](https://openai.com/research/whisper) — audio transcription
- [GPT-4o-mini](https://openai.com/api/) — translation
- Bootstrap 5 — frontend styling
