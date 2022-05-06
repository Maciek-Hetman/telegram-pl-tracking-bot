import logging
from telegram.ext import Updater, CommandHandler
from TrackInpostParcel import TrackInpostParcel
from TrackParcelPP import TrackParcelPP
from TrackDHLParcel import TrackDHLParcel
from sys import argv as arg
from time import sleep
from threading import Thread

UPDATE_INTERVAL = 3600             # How often bot will check for updates (in seconds)
ENABLE_DHL_TRACKING = True
DHL_API_KEY = None

# Logger config
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

"""
This should look like that:
parcels = {
    '<user id>': {
        '<tracking_number>': [<carrier>, </track_history output>],
        ...
    },
    ...
}
Basically we check if track_history() output for given carrier and tracking number matches parcels['<user_id>']['<tracking_number>'][1]
If not we sent message to user using updater.bot.sendMessage(chat_id='<user_id>', text='package update: <new track_history output>')
Problem is when program stops running. Later on probably i'll make json file with it or sth
"""
parcels = {}

def check_parcels_daemon(updater, parcels, update_interval):
    for user_id in parcels:
        for tracking_number in parcels[user_id]:
            carrier = parcels[user_id][tracking_number][0]
        
        try:
            tracker = create_tracker(carrier, tracking_number)
        except UnboundLocalError:
            continue
        
        info = tracker.get_tracking_history()

        if info != parcels[user_id][tracking_number][1]:
            parcels[user_id][tracking_number][1] = info
            updater.bot.sendMessage(chat_id=user_id, text="Package %s new status is:\n%s" % (tracking_number, tracker.get_current_status()))

    sleep(update_interval)


def create_tracker(carrier, tracking_number):
    if "poczta" in carrier.lower() or "pp" in carrier.lower():
        return TrackParcelPP(tracking_number)
    elif "inpost" in carrier.lower():
        return TrackInpostParcel(tracking_number)
    elif DHL_API_KEY != None and "dhl" in carrier.lower():
        return TrackDHLParcel(tracking_number, DHL_API_KEY)
    else:
        raise UnboundLocalError("Carrier not supported")


def start(update, context):
    text = "Welcome! You can see status of your parcel with /status <tracking number> <carrier> command."
    update.message.reply_text(text)
    carriers(update, context)
    text2 = "Use /help to see all available commands"
    update.message.reply_text(text2)


def help(update, context):
    # Don't look at this
    line1 = "/start - see welcome message"
    line2 = "\n/help - see this message"
    line3 = "\n/carriers - list supported carriers"
    line4 = "\n/status <tracking number> <carrier> - see current parcel status"
    line5 = "\n/track_history <tracking_number> <carrier> - see history of parcel"

    # Nothing to see here
    text = line1 + line2 + line3 + line4 + line5

    update.message.reply_text(text)


def carriers(update, context):
    line1 = "Currently supported carriers:"
    line2 = "\n\t- Poczta Polska (you can short it to 'pp')"
    line3 = "\n\t- InPost"
    line4 = "\nYou don't have to capitalize letters (inpost will be recognized as InPost)"

    text = line1 + line2 + line3 + line4

    update.message.reply_text(text)


def error(update, context):
    logger.warning('Update %s caused error "%s"' % (update, context.error))


def save(update, context):
    user_id = update.message.from_user['id']

    if len(context.args) >= 2:
        tracking_number = context.args[0]


        carrier = ""

        if len(context.args) == 2:
            carrier = context.args[1]
        else:
            for i in range(1, len(context.args)-1):
                carrier = carrier + context.args[i] + " "
    else:
        return update.message.reply_text('No tracking number/carrier provided.\nUse /status <tracking_number> <carrier>')        
    
    try:
        tracker = create_tracker(carrier, tracking_number)
    except UnboundLocalError:
        return update.message.reply_text("Carrier %s is not supported." % carrier)

    info = tracker.get_current_status()

    if user_id in parcels:
        if tracking_number in parcels[user_id]:
            try:
                parcels[user_id][tracking_number][0] = carrier
                parcels[user_id][tracking_number][1] = tracker.get_tracking_history()
            except IndexError:
                parcels[user_id][tracking_number] = [carrier, tracker.get_tracking_history()]
        
        else:
            parcels[user_id][tracking_number] = [carrier, tracker.get_tracking_history()]
    else:
        parcels[user_id] = {tracking_number: [carrier, tracker.get_tracking_history()]}
    
    update.message.reply_text("Parcel info saved")


def status(update, context):
    if len(context.args) >= 2:
        tracking_number = context.args[0]


        carrier = ""

        if len(context.args) == 2:
            carrier = context.args[1]
        else:
            for i in range(1, len(context.args)-1):
                carrier = carrier + context.args[i] + " "
    else:
        return update.message.reply_text('No tracking number/carrier provided.\nUse /status <tracking_number> <carrier>')        
    
    try:
        tracker = create_tracker(carrier, tracking_number)
    except UnboundLocalError:
        return update.message.reply_text("Carrier %s is not supported." % carirer)

    info = tracker.get_current_status()
    update.message.reply_text(info)


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
        return update.message.reply_text('No tracking number/carrier provided.\nUse /status <tracking_number> <carrier>')        
    
    try:
        tracker = create_tracker(carrier, tracking_number)
    except UnboundLocalError:
        return update.message.reply_text("Carrier %s is not supported." % carrier)

    info = tracker.get_tracking_history()
    update.message.reply_text(info)


def main(BOT_KEY, dhl_api_key=None):
    if dhl_api_key != None:
        DHL_API_KEY = dhl_api_key

    updater = Updater(BOT_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("carriers", carriers))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("track_history", track_history))
    dp.add_handler(CommandHandler("save", save))
    dp.add_error_handler(error)
    
    updater.start_polling()

    # Starting daemon
    ParcelDaemon = Thread(target=check_parcels_daemon(updater, parcels, UPDATE_INTERVAL))
    ParcelDaemon.setDaemon(True)
    ParcelDaemon.start()


if __name__ == '__main__':
    try:
        if len(arg) > 2:
            main(arg[1], arg[2])
        else:
            logger.log(20, "DHL tracking is disabled")
            main(arg[1])   
    except IndexError:
        logger.error("No bot token given.\nUsage: python3 main.py <bot token> <dhl api key>")
