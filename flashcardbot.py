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
from handlers import OPTION, NEW_WORD, EDIT_WORD

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def get_token():
    token = None
    try:
        token = os.getenv("TOKEN")
    except:
        try:
            with open('token.yml', 'r') as f:
                token = f.readline()
        except:
            print("The token should be written in token.yml")
            sys.exit(1)
    return token


def set_run(token):

    try:
        MODE = os.getenv("MODE")
    except:
        logger.error("No MODE specified!")
        sys.exit(1)

    if MODE == "dev":
        def run(updater):
            updater.start_polling()
            updater.idle()
    elif MODE == "prod":
        def run(updater):
            PORT = int(os.environ.get("PORT", "8443"))
            HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
            # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
            updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=token)
            updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, token))
    else:
        logger.error("No MODE specified!")
        sys.exit(1)
    return run, MODE


def main():

    token = get_token()
    run, MODE = set_run(token)

    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', handlers.start)],

        states={
            OPTION: [MessageHandler(Filters.regex('^Add flashcard$'), handlers.ask_flashcard),
                     MessageHandler(Filters.regex('^See flashcards$'), handlers.see_flashcards),
                     MessageHandler(Filters.regex('^Delete flashcard$'), handlers.ask_edit_flashcard),
                     MessageHandler(Filters.regex('^Review flashcards$'), handlers.review_flashcards),
                     MessageHandler(Filters.regex('^go$'), handlers.review_flashcards)],

            NEW_WORD: [MessageHandler(Filters.text, handlers.save_info)],
            EDIT_WORD: [MessageHandler(Filters.text, handlers.delete_flashcards)]
        },

        fallbacks=[MessageHandler(Filters.regex('^Done$'), handlers.done)],
        name="flashcard_bot"
    )

    dp.add_handler(conv_handler)
    dp.add_error_handler(handlers.error)

    logger.info(f"Starting bot in mode={MODE}")
    run(updater)


if __name__ == '__main__':
    main()
