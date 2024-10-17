import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
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
async def is_user_in_channel(context: CallbackContext, user_id):
    try:
        chat_member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return chat_member.status in ['member', 'administrator', 'creator']
    except:
        return False

# Start command
async def start(update: Update, context: CallbackContext):
    user = update.message.from_user

    # Check if user has joined the channel
    if await is_user_in_channel(context, user.id):
        await update.message.reply_text(f"Welcome {user.first_name}! You are a member of the channel {CHANNEL_ID}. Type /help to see available commands.")
    else:
        await update.message.reply_text(f"Please join the channel {CHANNEL_ID} to proceed.")

# Help command
async def help_command(update: Update, context: CallbackContext):
    help_message = """
    **Welcome to the AI Image Generator Bot!**

    Here are the commands you can use:

    - `/image <prompt>`: Generate an image based on your prompt using DALL-E 3.
    - `/help`: Display this help message.

    Example: `/image sunset on a beach`
    """
    await update.message.reply_text(help_message)

# Command to generate an image using DALL-E 3 API
async def generate_image(update: Update, context: CallbackContext):
    user = update.message.from_user
    prompt = ' '.join(context.args)

    if not prompt:
        await update.message.reply_text("Please provide a prompt to generate an image. Example: `/image sunset on a beach`")
        return

    # Check if user has joined the channel
    if not await is_user_in_channel(context, user.id):
        await update.message.reply_text(f"Please join the channel {CHANNEL_ID} to use this feature.")
        return

    # Generate the image using DALL-E 3 API
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,  # Number of images to generate
            size="1024x1024"  # Image size, you can change this as needed
        )

        image_url = response['data'][0]['url']
        await update.message.reply_photo(photo=image_url, caption=f"Here is your image for '{prompt}'")

    except Exception as e:
        await update.message.reply_text(f"An error occurred while generating the image: {e}")

# Main function to set up the bot and handlers
async def main():
    # Initialize the application using ApplicationBuilder (new in python-telegram-bot 20.x)
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Handlers for commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("image", generate_image))

    # Start the Bot
    await application.start_polling()
    await application.idle()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
