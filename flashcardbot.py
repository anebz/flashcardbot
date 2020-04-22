#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'anebz'

"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import os
import sys
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, PicklePersistence

import handlers

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

OPTION, NEW_WORD = range(2)

def main():
    # Create the Updater and pass it your bot's token.
    pp = PicklePersistence(filename='flashcard.pkl')

    token = None
    try:
        with open('token.yml', 'r') as f:
            token = f.readline()
    except:
        print("The token should be written in token.yml")
        sys.exit(1)

    updater = Updater(token, persistence=pp, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', handlers.start)],

        states={
            OPTION: [MessageHandler(Filters.regex('^Add flashcard$'), handlers.ask_flashcard),
                     MessageHandler(Filters.regex('^Review flashcards$'), handlers.review_flashcards)],

            NEW_WORD: [MessageHandler(Filters.text, handlers.save_info)]
        },

        fallbacks=[MessageHandler(Filters.regex('^Done$'), handlers.done)],
        name="flashcard_bot",
        persistent=True
    )

    dp.add_handler(conv_handler)
    #dp.add_handler(CommandHandler('show_data', show_data))
    dp.add_error_handler(handlers.error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
