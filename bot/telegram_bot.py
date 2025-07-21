from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
from dotenv import load_dotenv
import logging

from core.language_router import LanguageRouter
from services.google_translate import GoogleTranslateService # Assuming GoogleTranslateService is the default
from bot.session_state import set_user_lang, get_user_lang

# Get logger for this module
logger = logging.getLogger(__name__)

# Initialize the router globally
translation_engine = GoogleTranslateService()
router = LanguageRouter(engine=translation_engine)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "*Kannada ↔ Hindi ↔ English Translation Bot*\n\n"
        "Hello! Send me a message to translate.\n"
        "ನಮಸ್ಕಾರ! ಭಾಷಾಂತರಿಸಲು ನನಗೆ ಸಂದೇಶ ಕಳುಹಿಸಿ.\n"
        "नमस्ते! अनुवाद करने के लिए मुझे एक संदेश भेजें।\n\n"
        "Type `/help` for commands.",
        parse_mode="Markdown"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "*Kannada ↔ Hindi ↔ English Translation Bot*\n\n"
        "*Commands:*\n"
        "`/lang <code>` — Set your output language (e.g., `kn`, `hi`, `en`).\n"
        "`/start` — Welcome message.\n"
        "`/help` — This message.\n\n"
        "Just send a message to translate!",
        parse_mode="Markdown"
    )

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if context.args:
        lang_code = context.args[0].lower()
        # Basic validation for now, can be expanded
        if lang_code in ["kn", "hi", "en"]:
            set_user_lang(user_id, lang_code)
            await update.message.reply_text(f"Your target language has been set to: {lang_code.upper()}")
            logger.info(f"User {user_id} set target language to {lang_code}")
        else:
            await update.message.reply_text("Invalid language code. Please use 'kn' (Kannada), 'hi' (Hindi), or 'en' (English).")
            logger.warning(f"User {user_id} tried to set invalid language: {lang_code}")
    else:
        current_lang = get_user_lang(user_id)
        await update.message.reply_text(f"Your current target language is: {current_lang.upper()}. Use /lang <code_here> to change it.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id
    
    try:
        translated = router.translate(text, user_id)
        # The router now handles the source and target language logic internally
        # We can still display the user's current target language preference
        user_target_lang = get_user_lang(user_id)
        await update.message.reply_text(
            f"""*Translated* ({user_target_lang.upper()}):
_{translated}_

*Original*:
{text}""",
            parse_mode="Markdown"
        )
        logger.info(f"Translated '{text}' for user {user_id} to {user_target_lang}")
    except Exception as e:
        logger.error(f"Translation error for user {user_id} (message: '{text}'): {e}")
        await update.message.reply_text("⚠️ Sorry, translation failed. Try again later.")

def launch_bot(token: str):
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not provided.")
        print("Error: TELEGRAM_BOT_TOKEN not provided.")
        print("Please set the token before running the bot.")
        return

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("lang", set_language))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("✅ Bot is running...")
    app.run_polling()