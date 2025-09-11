import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
import threading
import os

# Get bot token from environment variable
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Create Flask app for Railway
app = Flask(__name__)

@app.route('/')
def keep_alive():
    return "🌹 Rose Bot is running! 🌹"

@app.route('/health')
def health():
    return "🌹 Rose Telegram Bot is healthy! 🌹"

def run_flask():
    """Run Flask app"""
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)

# Bot handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    welcome_message = """
🌹 **Welcome to Rose Bot!** 🌹

I'm here to welcome new members to your group!

**Commands:**
/start - Show this message
/help - Show help

**Add me to your group and I'll welcome everyone!** 🌹
    """
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_message = """
🌹 **Rose Bot Help** 🌹

**How to use:**
1. Add me to your group
2. Give me permission to read/send messages
3. I'll welcome new members automatically!

**Commands:**
/start - Welcome message
/help - This help

🌹 That's it! No setup needed! 🌹
    """
    await update.message.reply_text(help_message, parse_mode='Markdown')

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome new members"""
    message = update.message
    
    if message.new_chat_members:
        for new_member in message.new_chat_members:
            if not new_member.is_bot:
               welcome_text = f"hey @{new_member.username or new_member.first_name} welcome to the chat\n\nplease introduce yourself and what you are working on"
                await message.reply_text(welcome_text)
                print(f"✅ Welcomed: {new_member.first_name}")

def main():
    """Start the bot"""
    print("🌹 Rose Bot Starting...")
    
    if not BOT_TOKEN:
        print("❌ Error: BOT_TOKEN not found!")
        return
    
    # Start Flask in background
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Create bot application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
    
    print("🌹 Rose Bot is running! 🌹")
    
    # Start polling
    application.run_polling(
        poll_interval=1.0,
        timeout=10,
        drop_pending_updates=True
    )

if __name__ == '__main__':
    main()
