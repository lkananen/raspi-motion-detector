import telegram
import config

bot = telegram.Bot(token=config.telegram_bot_token)
bot.sendMessage(chat_id=config.bot_chat_id, text="Hello world!")

