# LLM Apps with Chainlit — Zomato OrderBot

An AI-powered food ordering chatbot built with Chainlit and OpenAI. The bot greets customers, takes their order from the menu, handles pickup/delivery, and calculates the final payment.

## Tech Stack

- **Python** — application logic
- **Chainlit** — chat UI framework
- **OpenAI** — `gpt-4o-mini` for conversational ordering

---

## How to Run

### Step 1 — Create and activate a conda environment

```bash
conda create -n chainlit-app python=3.10 -y
conda activate chainlit-app
```

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Set up environment variables

Create a `.env` file in the project root:

```ini
OPENAI_API_KEY=your_openai_api_key_here
```

### Step 4 — Run the app

```bash
chainlit run app.py
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## Features

- Per-session conversation history (each browser tab is isolated)
- Welcome greeting on chat start
- Full Zomato menu with Pizzas, Pasta, Asian, Indian cuisines and Beverages
- Handles pickup and delivery orders with address collection
- Calculates and summarizes the final order with payment

## Sample Questions

- *"I'd like to order a Pepperoni Pizza"*
- *"What's on the menu?"*
- *"I'll have Butter Chicken with Naan and a Mango Lassi"*
- *"Make it a delivery to 123 Main Street"*
