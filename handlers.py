import os
import sys
import logging
from random import sample
from pymongo import MongoClient

from telegram import ReplyKeyboardMarkup, ParseMode, Message
from telegram.ext import ConversationHandler

logger = logging.getLogger(__name__)

reply_keyboard = [['Add flashcard', 'See flashcards'], ['Delete flashcard', 'Review flashcards'], ['Done']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
OPTION, NEW_WORD, EDIT_WORD = range(3)

try:
    MONGODB_URL = os.getenv('MONGODB_URL')
except:
    print("No MONGO_URL found in the environment variables")
    sys.exit(1)

client = MongoClient(MONGODB_URL)
db = client.flashcardb
coll = db.flashcardb


def start(update, context):
    reply_text = "Hi! I'm the flashcard bot."
    if context.user_data:
        reply_text += " You already have some flashcards saved. Do you want to review them?"
    reply_text += " Do you want to add new words?"
    update.message.reply_text(reply_text, reply_markup=markup)

    return OPTION


def ask_flashcard(update, context):
    reply_text = "Write the new word you want to add to the flashcard system and the context "\
                 "in this format: incredible=this yoghurt is incredible"
    update.message.reply_text(reply_text)

    return NEW_WORD


def save_info(update, context):
    text = update.message.text.split("=")
    if len(text) != 2:
        update.message.reply_text("Please write the new word and context in this format: "
                                  "incredible=this yoghurt is incredible")
        return OPTION

    new_word, word_context = text[0], ''.join(text[1:])
    #context.user_data[new_word] = word_context
    reply_text = f"New word added: '{new_word}' with context: '{word_context}'"
    logger.info(reply_text)
    update.message.reply_text(reply_text, reply_markup=markup)

    # updates the 'flashcards' dictionary in mongodb https://docs.mongodb.com/manual/reference/operator/update/set/
    coll.update_one({'user_id': update.message.from_user.id},
                    {'$set': {'flashcards.'+new_word: word_context}}, upsert=True)

    return OPTION


def see_flashcards(update, context):
    # https://stackoverflow.com/questions/8885663/how-to-format-a-floating-number-to-fixed-width-in-python
    reply_text = "| id | word | word_context |" + "\n| --|:--:| --:|\n"

    user_data = coll.find_one({"user_id": update.message.from_user.id})[
        'flashcards']

    for i, (word, word_context) in enumerate(user_data.items()):
        reply_text += f"| {i+1} | {word} | {word_context} |\n"

    update.message.reply_text(reply_text)
    return OPTION

def ask_edit_flashcard(update, context):
    update.message.reply_text("Write the word you want to edit from the flashcard system")
    return EDIT_WORD


def delete_flashcards(update, context):
    word = update.message.text
    '''
    if word in context.user_data:
        reply_text = f"The word {word} was deleted"
        logger.info(reply_text)
        del context.user_data[word]
    else:
        reply_text = "This word is not in the flashcard system"
    '''
    coll.update_one({'user_id': update.message.from_user.id},
                    {'$unset': {'flashcards.'+word: ''}}, upsert=True)

    update.message.reply_text(f"The word {word} was deleted")
    return OPTION


def review_flashcards(update, context):
    if not context.user_data:
        update.message.reply_text("There are no saved flashcards")
        return OPTION
    
    all_words = sample(context.user_data.keys(), len(context.user_data))

    if not 'reviewing' in context.user_data:
        if not 'reviewed' in context.user_data:
            # beginning of review
            word = all_words[0]
            update.message.reply_text("You will see a word and try to remember its context. When you are ready, enter 'go'. \n"
                                      f"| word | word_context |\n| --|:--:| --:|\n| {word} | ... |\n")

        else:
            # some words have been reviewed, but none right now
            for possible_word in all_words:
                if possible_word != 'reviewed' and possible_word not in context.user_data['reviewed']:
                    # review a word that hasn't been reviewed yet
                    word = possible_word
                    update.message.reply_text(f"| {word} | ... |\n")
                    break
            else:
                # end of review
                update.message.reply_text("flashcard review complete")
                context.user_data.pop("reviewed", None)
                return OPTION

        context.user_data['reviewing'] = word
        logger.info(f"Reviewing word {word}")

    else:
        # the user is reviewing one word
        reviewing_word = context.user_data['reviewing']
        update.message.reply_text(f"| {reviewing_word} | {context.user_data[reviewing_word]} |\n")
        logger.info(f"Reviewing context of word {reviewing_word}")

        if not 'reviewed' in context.user_data:
            context.user_data['reviewed'] = [reviewing_word]
        else:
            context.user_data['reviewed'].append(reviewing_word)

        context.user_data.pop('reviewing', None)
        review_flashcards(update, context)

    return OPTION


def done(update, context):
    context.user_data.pop("reviewing", None)
    context.user_data.pop("reviewed", None)
    logger.info("Session ended")
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
