# DALL-E Image Generator

A Flask web app that generates images from text prompts using OpenAI's DALL-E 2 model.

## How It Works

```
User enters a text prompt → DALL-E 2 generates 5 images → Images displayed in the browser
```

## Features

- Generate 5 images at a time from a text prompt
- 256x256 image resolution
- Loading spinner while images are being generated
- Clean Bootstrap 5 UI

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

1. Type a descriptive prompt in the text box
2. Click **Submit**
3. Wait for the images to generate and appear on screen

## Tech Stack

- [Flask](https://flask.palletsprojects.com/) — web framework
- [OpenAI DALL-E 2](https://openai.com/dall-e-2) — image generation
- Bootstrap 5 — frontend styling
