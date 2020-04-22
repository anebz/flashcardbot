#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, PicklePersistence

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

reply_keyboard = [['Add flashcard', 'Review flashcards'], ['Done']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
OPTION, NEW_WORD = range(2)


def start(update, context):
    reply_text = "Hi! I'm the flashcard bot."
    if context.user_data:
        reply_text += " You already have some flashcards saved. Do you want to review them?"
    reply_text += " Do you want to add new words?"
    update.message.reply_text(reply_text, reply_markup=markup)

    return OPTION

def ask_flashcard(update, context):
    reply_text = "Write the new word you want to add to the flashcard system and the context "\
                 "in this format: 'incredible''this yoghurt is incredible'"
    update.message.reply_text(reply_text)

    return NEW_WORD

def save_info(update, context):
    text = update.message.text.split('.')
    # TODO do this as regex to check that the second part is a sentence of letters.
    if len(text) < 2 or (len(text) == 2 and len(text[1]) < len(text[0])):
        update.message.reply_text("Please write the new word and context "\
                                  "in this format: 'incredible''this yoghurt is incredible'")
        return OPTION

    new_word = text[0]
    word_context = '. '.join(text[1:])
    context.user_data[new_word] = word_context
    reply_text = f"New word added: '{new_word}' with context:'{word_context}'"
    logger.info(reply_text)

    update.message.reply_text(reply_text, reply_markup=markup)
    return OPTION

def review_flashcards(update, context):
    reply_text = "id\tword\tword_context\n"
    reply_text += '\n'.join([f"{i+1}\t{word}\t{word_context}" for i, (word, word_context) in enumerate(context.user_data.items())])
    logger.info(reply_text)

    update.message.reply_text(reply_text, reply_markup=markup)
    return OPTION

def done(update, context):
    logger.info("Session ended.")
    return ConversationHandler.END

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    # Create the Updater and pass it your bot's token.
    pp = PicklePersistence(filename='flashcard.pkl')

    token = None
    try:
        with open('token.yml') as f:
            token = f.readline()
    except:
        print("The token should be written in token.yml")
        sys.exit(1)

    updater = Updater(token, persistence=pp, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            OPTION: [MessageHandler(Filters.regex('^Add flashcard$'), ask_flashcard),
                     MessageHandler(Filters.regex('^Review flashcards$'), review_flashcards)],

            NEW_WORD: [MessageHandler(Filters.text, save_info)]
        },

        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
        name="flashcard_bot",
        persistent=True
    )

    dp.add_handler(conv_handler)
    #dp.add_handler(CommandHandler('show_data', show_data))
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
