import logging
from bot.telegram_bot import launch_bot
from config.settings import settings

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    launch_bot(settings.TELEGRAM_BOT_TOKEN)