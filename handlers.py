import logging
from telegram import ReplyKeyboardMarkup, ParseMode, Message
from telegram.ext import ConversationHandler

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
        update.message.reply_text("Please write the new word and context "
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
    update.message.reply_text(reply_text)
    return OPTION


def done(update, context):
    logger.info("Session ended.")
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
