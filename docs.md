# KTranslate Bot - Developer Documentation

## 1. Introduction

### 1.1. Project Overview
KTranslate Bot is a multilingual translation chatbot designed to operate on messaging platforms like Telegram and WhatsApp. It provides seamless translation between Kannada, English, and Hindi, aiming to bridge communication gaps in digital conversations. The project is built with Python and leverages various translation services, including modern LLM-based approaches.

### 1.2. Core Problem Solved
The bot addresses the need for accessible and accurate translation in multilingual communities, particularly for users who are more comfortable with regional languages like Kannada. It helps in understanding and responding to messages in different languages, making digital communication more inclusive.

### 1.3. Key Features
- **Multilingual Translation:** Supports Kannada, English, and Hindi.
- **Platform Integration:** Designed for Telegram and can be extended to WhatsApp.
- **Flexible Translation Engine:** Utilizes a core translation engine that can integrate with multiple backend services like Google Translate, IndicTrans2, and Bhashini.
- **API Server:** An optional FastAPI server provides REST endpoints for translation, allowing the core logic to be used by other applications.
- **Docker Support:** Comes with Dockerfiles for easy containerization and deployment.

## 2. System Architecture

### 2.1. High-Level Diagram
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

### 2.2. Component Breakdown
- **Telegram/Whatsapp Bot (`bot/`):** This is the user-facing component that handles incoming messages from the chat platform and sends back the translated text.
- **API Server (`api/`):** A FastAPI application that exposes the translation functionality through a REST API. This allows for web-based clients or other services to use the translation engine.
- **Core Logic (`core/`):** This is the heart of the application. It includes the `language_router.py` for a unified interface to the various translation services.
- **Services (`services/`):** These are pluggable modules for different translation backends. Each service wrapper (e.g., `google_translate.py`, `indictrans2_service.py`) adheres to a common interface, making it easy to switch between or add new translation providers.

### 2.3. Data Flow
1. A user sends a message to the bot on a chat platform.
2. The bot handler (`telegram_bot.py`) receives the message.
3. The message is passed to the `language_router.py` in the core logic to detect the source language.
4. The `translation_engine.py` is called with the text, source language, and target language.
5. The engine routes the request to one of the configured translation services in the `services/` directory.
6. The translation service returns the translated text.
7. The bot handler sends the translated text back to the user.

## 3. Getting Started

### 3.1. Prerequisites
- Python 3.8+
- Docker and Docker Compose (for containerized setup)
- Access to a Telegram Bot Token

### 3.2. Local Installation

#### 3.2.1. Cloning the Repository
```bash
git clone https://github.com/your-username/ktranslate.git
cd ktranslate
```

#### 3.2.2. Setting up the Python Environment
It is highly recommended to use a virtual environment.
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 3.2.3. Environment Variables
Create a `.env` file in the root directory of the project and add the following, replacing the placeholder values with your actual credentials.
```ini
# .env file
GOOGLE_API_KEY="your_google_api_key"
INDIC_MODEL_PATH="/path/to/your/indictrans_model"
BHASHINI_API_KEY="your_bhashini_api_key"
TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
```
**Note:** The `.env` file is included in `.gitignore` and should not be committed to version control.

### 3.3. Running with Docker
The project includes `Dockerfile.bot` and `Dockerfile.api` for building container images for the bot and the API server, respectively. A `docker-compose.yml` file is also provided to orchestrate the services.
```bash
docker-compose up --build
```

## 4. Project Structure

### 4.1. Directory and File Overview
```
ktranslate/
├── bot/                            # Chatbot interface layer
│   ├── __init__.py
│   ├── telegram_bot.py             # Telegram bot handler (receives messages, replies)
│   └── whatsapp_bot.py             # (Optional) WhatsApp integration via Twilio/Meta API
│
├── core/                           # Core NLP and translation routing logic
│   ├── __init__.py
│   ├── translation_engine.py       # Unified interface to translation backends
│   ├── utils.py                    # Pre/post-processing: cleaning, normalization, etc.
│   └── language_router.py          # Detect source/target language, tone handling
│
├── services/                       # Translation engines (pluggable modules)
│   ├── google_translate.py         # Google Translate API wrapper
│   ├── indictrans2_service.py      # IndicTrans2 (HuggingFace or local inference)
│   └── bhashini_api.py             # Govt. of India Bhashini API (for Kannada/Hindi)
│
├── api/                            # (Optional) Web client or admin dashboard via FastAPI
│   ├── main.py                     # Entry for FastAPI server
│   └── routes.py                   # REST endpoints (e.g., `/translate`)
│
├── data/                           # Input/output samples, evaluation data
│   └── test_phrases.csv            # List of test sentences for benchmarking
│
├── database/                       # DB schema + persistence layer (if used)
│   ├── models.py                   # SQLAlchemy models for users, logs, etc.
│   └── crud.py                     # Create/Read/Update/Delete DB ops
│
├── experiments/                    # Translation quality, prompt tuning, evals
│   └── test_google_vs_indictrans.ipynb  # Notebook comparing engines
│
├── config/                         # Global constants and API keys (use dotenv or pydantic)
│   └── settings.py
│
├── tests/                          # Unit + integration tests
│   └── test_translation.py         # Sample tests for translation and routing logic
│
├── requirements.txt                # Python dependencies
├── README.md                       # Project overview and usage instructions
└── run_bot.py                      # Main entry point to launch bot (Telegram by default)
```

## 5. Core Components in Detail

### 5.1. `bot/`
This directory contains the user-facing part of the bot.

-   **`telegram_bot.py`**: This script contains the main logic for the Telegram bot. It uses the `python-telegram-bot` library to handle commands (`/start`, `/help`, `/lang`) and messages. It initializes the `LanguageRouter` and calls it to process incoming text for translation. It also manages user-specific language preferences through the `session_state` module.
-   **`whatsapp_bot.py`**: This is a placeholder for a potential WhatsApp integration.
-   **`session_state.py`**: A simple in-memory session manager to store user-specific data, like the preferred target language.

### 5.2. `core/`
This is where the main business logic of the application resides.

-   **`language_router.py`**: This module is responsible for detecting the language of the input text using the `langdetect` library. It then determines the source and target languages for the translation based on the user's preferred language (fetched from `session_state`). A key feature is its ability to "invert" the translation if the user writes in their target language (e.g., if the target is 'en' and the user writes in English, it will translate to Kannada by default).
-   **`translation_engine.py`**: This file defines the abstract base class `TranslationEngine`. All translation services must inherit from this class and implement the `translate` method. This ensures a consistent interface for the `LanguageRouter` to use, regardless of which translation service is active.

### 5.3. `services/`
This directory contains the concrete implementations of the `TranslationEngine`.

-   **`google_translate.py`**: A wrapper for the `deep-translator` library, which uses the Google Translate API.
-   **`indictrans2_service.py`**: An implementation that uses the `IndicTrans2` model from Hugging Face's `transformers` library. This is suitable for high-quality translations involving Indian languages. Note that it requires a specific model and tokenizer, and the input text needs to be formatted with a special language token (e.g., `<2kn>`).
-   **`bhashini_api.py`**: A placeholder for an implementation that would use the Indian government's Bhashini translation service.

### 5.4. `api/`
This directory contains the code for the optional FastAPI server.

-   **`main.py`**: The entry point for the FastAPI application. It creates the FastAPI app instance and includes the router from `routes.py`.
-   **`routes.py`**: Defines the API endpoints. Currently, it includes a `/health` endpoint for health checks. This can be extended to include a `/translate` endpoint that exposes the core translation logic over HTTP.

## 6. Configuration

### 6.1. `config/settings.py`
This file uses `pydantic-settings` to manage configuration. It loads environment variables from a `.env` file. The `Settings` class defines the expected environment variables, ensuring that the application has the necessary configuration to run.

### 6.2. Required API Keys and Tokens
All secrets, such as the `TELEGRAM_BOT_TOKEN` and API keys for various translation services, should be stored in the `.env` file in the root directory. This file is ignored by Git, so it's a safe place to keep sensitive information.

## 7. How to Run

### 7.1. Running the Bot
The main entry point for the bot is `run_bot.py`. This script imports the necessary configurations and starts the Telegram bot.
```bash
python run_bot.py
```

### 7.2. Running the API
The FastAPI server can be started using `uvicorn`. This is useful for testing the API endpoints or for deploying the API as a separate service.
```bash
uvicorn api.main:app --reload
```

### 7.3. Running Tests
The project uses Python's built-in `unittest` framework. The tests are located in the `tests/` directory. To run the tests, use the following command:
```bash
python -m unittest discover tests
```

## 8. Contributing

### 8.1. Code Style and Conventions
Please follow the PEP 8 style guide for Python code. Ensure that your code is well-commented, especially in complex areas.

### 8.2. Submitting Changes (Pull Requests)
1.  Fork the repository.
2.  Create a new branch for your feature or bug fix (`git checkout -b feature/my-new-feature`).
3.  Make your changes and commit them with a clear and descriptive commit message.
4.  Push your branch to your fork (`git push origin feature/my-new-feature`).
5.  Open a pull request to the `main` branch of the original repository.

### 8.3. Adding a New Translation Service
To add a new translation service, follow these steps:
1.  Create a new file in the `services/` directory (e.g., `my_translation_service.py`).
2.  In the new file, create a class that inherits from `core.translation_engine.TranslationEngine`.
3.  Implement the `translate(self, text: str, src_lang: str, tgt_lang: str) -> str` method in your class.
4.  In `bot/telegram_bot.py` or wherever the `LanguageRouter` is initialized, you can now instantiate your new service and pass it to the router.

## 9. Deployment

### 9.1. Docker Compose
The most straightforward way to deploy the application is with Docker Compose. The `docker-compose.yml` file defines the `bot` and `api` services.
```bash
docker-compose up --build -d
```
This command will build the Docker images and run the services in the background.

### 9.2. Manual Deployment
You can also build and run the Docker images manually.

**For the bot:**
```bash
docker build -t ktranslate-bot -f Dockerfile.bot .
docker run -d --env-file .env ktranslate-bot
```

**For the API:**
```bash
docker build -t ktranslate-api -f Dockerfile.api .
docker run -d -p 8000:8000 ktranslate-api
```

## 10. Troubleshooting

### 10.1. Common Issues
-   **`ModuleNotFoundError`**: Make sure you have activated the correct Python virtual environment and that all the dependencies from `requirements.txt` are installed.
-   **Authentication Errors**: Verify that your API keys and tokens in the `.env` file are correct and that they have the necessary permissions.
-   **Bot not responding**: Check the logs for any errors. Ensure that the `TELEGRAM_BOT_TOKEN` is correct and that the bot is running.

### 10.2. Logging and Debugging
The application uses Python's standard `logging` module. The log level is configured in `run_bot.py`. When debugging, you can check the console output for logs that can help you identify the source of the problem.
