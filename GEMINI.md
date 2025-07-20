## GEMINI.md – Kannada Translation Bot (Telegram)

This is a development reference log for building a **Telegram chatbot** in **Python**, assisted by **Gemini CLI**.
The bot helps users translate between **Kannada, English, and Hindi** — with clarity, context, and accessibility.

---

## Project Overview

The goal is to create a multilingual assistant bot that:
- Accepts user messages in any of the three languages
- Detects the input language
- Returns a clean, grammatically correct translation to the desired language

Use cases include:
- Kannada-speaking users replying to English/Hindi messages
- Translating official messages for better understanding
- Reducing communication gaps in multilingual digital spaces

Tools used:
- Gemini CLI for prompt engineering and logic support
- Python as the bot engine
- Telegram Bot API for communication

---

## Architecture Overview

```
+------------------------+
|   User on Telegram     |
+-----------+------------+
            |
            v
+------------------------+
| Telegram Bot Webhook   |
| (python-telegram-bot)  |
+-----------+------------+
            |
            v
+-----------------------------+
| Language Detection Module   |
| (langdetect / heuristic)    |
+-----------+-----------------+
            |
            v
+-----------------------------+
| Translation Engine          |
| - Gemini Prompt (LLM)       |
| - OR fallback API           |
+-----------+-----------------+
            |
            v
+------------------------+
| Translated Output Back     |
| to Telegram User           |
+------------------------+
```

---

## Core Functionalities

| Feature               | Description                                                  |
|----------------------|--------------------------------------------------------------|
| `/start` command     | Bot introduction and instructions                            |
| Message handler      | Receives all user messages                                   |
| Language detection   | Identifies Kannada, Hindi, English input                     |
| Gemini translation   | Uses prompt-based LLM translation                            |
| Fallback mechanism   | Calls external API if LLM fails or is unavailable            |
| Graceful handling    | Cleans up garbled inputs and retries translation             |

---

## Gemini Prompt (Example)

```
Translate the following message to [Target Language].
Ensure it is natural, grammatically correct, and suitable for messaging.
Clean up noisy or casual input if needed.

Input: "where nearest bus?"
Output: "ಹತ್ತಿರದ ಬಸ್ ನಿಲ್ದಾಣ ಎಲ್ಲಿದೆ?"
```

**Gemini CLI Command Format:**
```bash
gemini prompt "Write a Python function that detects language from text using langdetect and routes translation based on target language"
```

Use `--context` to insert relevant parts of your bot script for targeted suggestions.

---

## Tech Stack Summary

| Component             | Tool/Library                        |
|----------------------|-------------------------------------|
| Bot Framework        | `python-telegram-bot`               |
| Language Detection   | `langdetect`, regex fallback        |
| LLM Prompting        | `gemini` CLI                        |
| Translation Fallback | Google Translate API / IndicTrans2  |
| Deployment           | Local + Cloud (Render/Heroku)       |
| Environment Vars     | `.env`, `python-dotenv`             |

---

## Task Checklist

- [ ] Telegram bot token and webhook set up
- [ ] Message handler script written
- [ ] Language detection function in place
- [ ] Gemini prompt logic integrated
- [ ] Translation API fallback added
- [ ] Testing with real inputs (formal/informal)
- [ ] Deployment + demo readiness

---

## Gemini Usage Guide

To get help on submodules, use:
```bash
gemini prompt "Add language detection and routing logic for a multilingual Telegram bot"
```
Or with code context:
```bash
gemini prompt --context bot.py "Enhance this handler with LLM-based translation to Kannada"
```

---

## Notes

This bot supports inclusive, multilingual communication for Kannada users and learners. It makes technology accessible by integrating AI and language support in everyday messaging platforms.

Project maintained under ethical use. No data is stored; conversations are ephemeral.

