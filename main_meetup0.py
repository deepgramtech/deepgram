#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple inline keyboard bot with multiple CallbackQueryHandlers.
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined as callback query handler. Then, those functions are
passed to the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot that uses inline keyboard that has multiple CallbackQueryHandlers arranged in a
ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line to stop the bot.
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler
import logging
import requests
import re

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Stages
FIRST, SECOND = range(2)
# Callback data

ONE, TWO, THREE, FOUR, EARLYEND = range(5)


def fastinfo(update, context):
    bot = context.bot
    when = KeyboardButton("When?", callback_data="when")
    where = KeyboardButton("Where?", callback_data="where")
    what = KeyboardButton("What?", callback_data="what")
    bookit = KeyboardButton("Book it.", callback_data="bookit")
    custom_keyboard = [
                    [when, where],
                    [what, bookit]
                    ]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text="Click on the button to get the info", reply_markup=reply_markup)

def infos(update, context):
    query = update.callback_query
    print(query.data)
    if query.data == 'when':
        print('ciao')


def start(update, context):
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data=str(ONE)),
         InlineKeyboardButton("No", callback_data=str(TWO))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.message.reply_text(
        "Do you want to know more about DeepGram Meetups?",
        reply_markup=reply_markup
    )
    # Tell ConversationHandler that we're in state `FIRST` now
    return FIRST


def start_over(update, context):
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    # Get Bot from CallbackContext
    bot = context.bot
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data=str(ONE)),
         InlineKeyboardButton("No", callback_data=str(TWO))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Do you want to know more about DeepGram Meetups?",
        reply_markup=reply_markup
    )
    return FIRST


def one(update, context):
    """Show new choice of buttons"""
    query = update.callback_query
    bot = context.bot
    keyboard = [
        [InlineKeyboardButton("Just info.", callback_data=str(THREE)),
         InlineKeyboardButton("Book a free ticket for the next meetup", callback_data=str(FOUR))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Do you want just info or do you want to come to the next meetup?",
        reply_markup=reply_markup
    )
    return FIRST


def two(update, context):
    """Show new choice of buttons"""
    query = update.callback_query
    bot = context.bot
    keyboard = [
        [InlineKeyboardButton("Ok, tell me more", callback_data=str(ONE)),
         InlineKeyboardButton("I'm ok, I'm here for mistake.", callback_data=str(EARLYEND))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Well, then why are you here? Do you know that on Wednesday 16th we have another Meetup?",
        reply_markup=reply_markup
    )
    return FIRST

def info(update, context):
    query = update.callback_query
    bot = context.bot
    query.edit_message_text(text="Great! It is a Meetup we take every two weeks at Digital Tree (https://digitaltree.ai) to create a Telegram Bot to perform Deep Learning! Interesting, right? Learn more at deepgram.tech.")
    # Transfer to conversation state `SECOND`
    return ConversationHandler.END

def eventbrite(update, context):
    query = update.callback_query
    bot = context.bot
    query.edit_message_text(text="You are doing right! Book it here: https://www.eventbrite.it/e/biglietti-deepgram1-creiamo-un-bot-per-il-deep-learning-76718881239")

    # Transfer to conversation state `SECOND`
    return ConversationHandler.END

def three(update, context):
    """Show new choice of buttons"""
    query = update.callback_query
    bot = context.bot
    keyboard = [
        [InlineKeyboardButton("Yes, let's do it again!", callback_data=str(ONE)),
         InlineKeyboardButton("Nah, I've had enough ...", callback_data=str(TWO))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Third CallbackQueryHandler. Do want to start over?",
        reply_markup=reply_markup
    )
    # Transfer to conversation state `SECOND`
    return SECOND


def four(update, context):
    """Show new choice of buttons"""
    query = update.callback_query
    bot = context.bot
    keyboard = [
        [InlineKeyboardButton("2", callback_data=str(TWO)),
         InlineKeyboardButton("4", callback_data=str(FOUR))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Fourth CallbackQueryHandler, Choose a route",
        reply_markup=reply_markup
    )
    return FIRST


def end(update, context):
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over"""
    query = update.callback_query
    bot = context.bot
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="See you next time!"
    )
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url

def get_image_url():
    allowed_extension = ['jpg','jpeg','png']
    file_extension = ''
    while file_extension not in allowed_extension:
        url = get_url()
        file_extension = re.search("([^.]*)$",url).group(1).lower()
    return url

def bop(bot, update):
    url = get_image_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("YOUR_TOKEN_HERE", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [CallbackQueryHandler(one, pattern='^' + str(ONE) + '$'),
                    CallbackQueryHandler(two, pattern='^' + str(TWO) + '$'),
                    CallbackQueryHandler(info, pattern='^' + str(THREE) + '$'),
                    CallbackQueryHandler(eventbrite, pattern='^' + str(FOUR) + '$'),
                    CallbackQueryHandler(end, pattern='^' + str(EARLYEND) + '$')],
            SECOND: [CallbackQueryHandler(end, pattern='^' + str(EARLYEND) + '$'),
                     CallbackQueryHandler(end, pattern='^' + str(EARLYEND) + '$')]
        },
        fallbacks=[CommandHandler('start', start)]
    )

    # Add ConversationHandler to dispatcher that will be used for handling
    # updates
    dp.add_handler(conv_handler)





    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
