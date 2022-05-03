#!/usr/local/bin/python3
import logging
from xdrlib import ConversionError
from setuptools import Command
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from TrackInpostParcel import TrackInpostParcel
from TrackParcel import TrackParcel
from sys import argv as arg

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Send message when /start command is issued
def start(update, context):
    text = "Hi!"

    update.message.reply_text(text)

# Send message when /help command is issued
def help(update, context):
    text = "/start - welcome message\n/track - track package"

    update.message.reply_text(text)

# Echo user message
def echo(update, context):
    update.message.reply_text(update.message.text)

# Log errors
def error(update, context):
    logger.warning('Update %s caused error "%s"' % (update, context.error))

def track(update, context):
    use_inpost_api = context.args[1].lower() == 'inpost'
    tracking_number = context.args[0]

    if use_inpost_api == False:
        tracker = TrackParcel(tracking_number)
        info = tracker.getStatus()
    else:
        tracker = TrackInpostParcel(tracking_number)
        info = tracker.getStatus()
    
    update.message.reply_text(info)

def main(BOT_KEY):
    updater = Updater(BOT_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("track", track))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)


    updater.start_polling()

if __name__ == '__main__':
    main(arg[1])
