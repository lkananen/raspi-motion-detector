import telegram
import config

bot = telegram.Bot(token=config.telegram_bot_token)
print(bot.get_me())
bot.sendMessage(chat_id=config.telegram_chat_id, text="Hello world!")

