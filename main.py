#!/usr/local/bin/python3
import logging
from telegram.ext import Updater, CommandHandler
from TrackInpostParcel import TrackInpostParcel
from TrackParcelPP import TrackParcelPP
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

# Log errors
def error(update, context):
    logger.warning('Update %s caused error "%s"' % (update, context.error))

# /track command
def track(update, context):
    if len(context.args) >= 2:
        tracking_number = context.args[0]
        carrier = ""

        if len(context.args) == 2:
            carrier = context.args[1]
        else:
            for i in range(1, len(context.args)-1):
                carrier = carrier + context.args[i] + " "
    else:
        return update.message.reply_text('No tracking number/carrier provided.\nUse /track <tracking_number> <carrier>')        
    
    if "poczta" in carrier.lower() or "pp" in carrier.lower():
        tracker = TrackParcelPP(tracking_number)
    elif "inpost" in carrier.lower():
        tracker = TrackInpostParcel(tracking_number)
    else:
        return update.message.reply_text("%s parcels are not supported" % carrier.capitalize())
        
    info = tracker.get_current_status()
    update.message.reply_text(info)

# /track_history command
def track_history(update, context):
    if len(context.args) >= 2:
        tracking_number = context.args[0]
        carrier = ""

        if len(context.args) == 2:
            carrier = context.args[1]
        else:
            for i in range(1, len(context.args)-1):
                carrier = carrier + context.args[i] + " "
    else:
        return update.message.reply_text('No tracking number/carrier provided.\nUse /track <tracking_number> <carrier>')        
    
    if "poczta" in carrier.lower() or "pp" in carrier.lower():
        tracker = TrackParcelPP(tracking_number)
    elif "inpost" in carrier.lower():
        tracker = TrackInpostParcel(tracking_number)
    else:
        return update.message.reply_text("%s parcels are not supported" % carrier.capitalize())

    info = tracker.get_tracking_history()
    update.message.reply_text(info)

def main(BOT_KEY):
    updater = Updater(BOT_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("track", track))
    dp.add_handler(CommandHandler("track_history", track_history))
    dp.add_error_handler(error)

    updater.start_polling()

if __name__ == '__main__':
    main(arg[1])
