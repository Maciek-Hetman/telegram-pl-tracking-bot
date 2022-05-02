#!/usr/local/bin/python3
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from PocztaPolskaAPI import PocztaPolska
from sys import argv as arg

print("Hello world")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Send message when /start command is issued
def start(update, context):
    update.message.reply_text("Hi!")

# Send message when /help command is issued
def help(update, context):
    update.message.reply_text("Help")

# Echo user message
def echo(update, context):
    update.message.reply_text(update.message.text)

# Log errors
def error(update, context):
    logger.warning('Update %s caused error "%s"' % (update, context.error))

def main(BOT_KEY):
    updater = Updater(BOT_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)

    updater.start_polling()

    poczta = PocztaPolska()
    print(poczta.CheckPackage("testp0"))

if __name__ == '__main__':
    main(arg[2])
