import telegram

# Adds upper level directory to the modules path.
# Allows relative import beyond current top-level package.
import os
import sys
import inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import config


print(config.telegram_bot_token)
# bot = telegram.Bot(token=config.telegram_bot_token)
# print(bot.get_me())
# bot.sendMessage(chat_id=config.telegram_chat_id, text="Hello world!")

