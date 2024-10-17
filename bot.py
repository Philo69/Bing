import logging
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
import openai

# Telegram Bot Token and OpenAI API Key (using the provided API key)
TELEGRAM_BOT_TOKEN = "7674552208:AAHQDQghD0SugvaMC8D9oZ5r6QxdEzwH1G4"
OPENAI_API_KEY = "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"

# Initialize OpenAI API key
openai.api_key = OPENAI_API_KEY

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

CHANNEL_ID = "@TechPiroBots"  # Ensure user joins this channel

# Function to check if user is a member of the channel
def is_user_in_channel(bot: Bot, user_id):
    try:
        chat_member = bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return chat_member.status in ['member', 'administrator', 'creator']
    except:
        return False

# Start command
def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    bot = context.bot

    # Check if user has joined the channel
    if is_user_in_channel(bot, user.id):
        update.message.reply_text(f"Welcome {user.first_name}! You are a member of the channel {CHANNEL_ID}. Type /help to see available commands.")
    else:
        update.message.reply_text(f"Please join the channel {CHANNEL_ID} to proceed.")

# Help command
def help_command(update: Update, context: CallbackContext):
    help_message = """
    **Welcome to the AI Image Generator Bot!**

    Here are the commands you can use:

    - `/image <prompt>`: Generate an image based on your prompt using DALL-E 3.
    - `/help`: Display this help message.

    Example: `/image sunset on a beach`
    """
    update.message.reply_text(help_message)

# Command to generate an image using DALL-E 3 API
def generate_image(update: Update, context: CallbackContext):
    user = update.message.from_user
    bot = context.bot
    prompt = ' '.join(context.args)

    if not prompt:
        update.message.reply_text("Please provide a prompt to generate an image. Example: `/image sunset on a beach`")
        return

    # Check if user has joined the channel
    if not is_user_in_channel(bot, user.id):
        update.message.reply_text(f"Please join the channel {CHANNEL_ID} to use this feature.")
        return

    # Generate the image using DALL-E 3 API
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,  # Number of images to generate
            size="1024x1024"  # Image size, you can change this as needed
        )

        image_url = response['data'][0]['url']
        update.message.reply_photo(photo=image_url, caption=f"Here is your image for '{prompt}'")

    except Exception as e:
        update.message.reply_text(f"An error occurred while generating the image: {e}")

# Main function to set up the bot and handlers
def main():
    # Set up the Updater
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Handlers for commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("image", generate_image))

    # Start the Bot
    updater.start_polling()

    # Run the bot until Ctrl-C is pressed
    updater.idle()

if __name__ == '__main__':
    main()
  
