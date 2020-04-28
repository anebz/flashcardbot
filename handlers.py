import logging
from telegram import ReplyKeyboardMarkup, ParseMode, Message
from telegram.ext import ConversationHandler

logger = logging.getLogger(__name__)

reply_keyboard = [['Add flashcard', 'See flashcards'], ['Delete flashcard', 'Done']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
OPTION, NEW_WORD, EDIT_WORD = range(3)


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
    text = update.message.text.split("''")
    # TODO do this as regex to check that the second part is a sentence of letters.
    if len(text) != 2 or text[0][0] != "'" or text[1][-1] != "'":
        update.message.reply_text("Please write the new word and context "
                                  "in this format: 'incredible''this yoghurt is incredible'")
        return OPTION

    new_word, word_context = text[0][1:], text[1][:-1]
    context.user_data[new_word] = word_context
    reply_text = f"New word added: '{new_word}' with context:'{word_context}'"
    logger.info(reply_text)

    update.message.reply_text(reply_text, reply_markup=markup)
    return OPTION


def review_flashcards(update, context):
    # https://stackoverflow.com/questions/8885663/how-to-format-a-floating-number-to-fixed-width-in-python
    reply_text = "| id | word | word_context |" + "\n| --|:--:| --:|\n"

    for i, (word, word_context) in enumerate(context.user_data.items()):
        reply_text += f"| {i+1} | {word} | {word_context} |\n"

    update.message.reply_text(reply_text)
    return OPTION

def ask_edit_flashcard(update, context):
    update.message.reply_text("Write the word you want to edit from the flashcard system")
    return EDIT_WORD


def delete_flashcards(update, context):
    word = update.message.text
    if word in context.user_data:
        reply_text = f"The word {word} was deleted"
        del context.user_data[word]
    else:
        reply_text = "This word is not in the flashcard system"

    update.message.reply_text(reply_text)
    return OPTION


def done(update, context):
    logger.info("Session ended.")
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
