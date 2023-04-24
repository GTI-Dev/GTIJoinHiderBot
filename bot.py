import telebot
import os
import telebot
from typing import Dict
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from dotenv import load_dotenv
load_dotenv()

# Get the bot token from an environment variable
bot_token = os.getenv('bot_token')

# Create a new bot instance
bot = telebot.TeleBot(bot_token)

# Define the user database
users = {}

# Define the supported languages and their messages
languages: Dict[str, Dict[str, str]] = {
    '🇬🇧 English': {
        'greeting': '👋 Hey!\n',
        'instructions': "\nI am Group Silencer Bot! \n\nTo use me, make me an admin and I will be able to delete all the pesky notification when a member joins or leaves the group! \n\n ➕ Please add me to your groups \n\n⛔️Give me delete permissions",
        'language_set': 'The language is changed to English',
    },
    '🇪🇹 አማርኛ ': {
        'greeting': '👋 ሰላም!\n',
        'instructions': '\nእኔ የቡድን ጸጥታ ጸጥታ አስከባሪ ቦት ነኝ! \n\nእኔን ለመጠቀም አስተዳዳሪ አድርገኝ እና አንድ አባል ከቡድኑ ሲቀላቀል ወይም ሲወጣ ሁሉንም ማስታወቂያዎች መሰረዝ እችላለሁ! \n\n ➕ እባክዎን ወደ ግሩፖ ላይ ያስገቡኝ \n\n⛔️የመሰረዝ ፈቃዶችን ይስጡኝ።',
        'language_set': 'ቋንቋው ወደ አማርኛ ተቀይሯል።',
    },
}


@bot.message_handler(content_types=['new_chat_members'])
def delete_join_message(message):
    # If bot is not admin, then it will not be able to delete message.
    try:
        if message.new_chat_member is not None and message.new_chat_member.id != bot.get_me().id:
            bot.delete_message(message.chat.id, message.message_id)
    except:
        if message.new_chat_member is not None and message.new_chat_member.id != bot.get_me().id:
            bot.send_message(
                message.chat.id, "Please make me an admin in order for me to remove the join and leave messages on this group!")
        else:
            bot.send_message(message.chat.id, "")


# Handler for users leaving the chat
@bot.message_handler(content_types=['left_chat_member'])
def delete_leave_message(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass


@bot.message_handler(commands=['start', 'language'])
def language_handler(message):
    chat_id = message.chat.id
    message_id = message.message_id
    user_id = message.chat.id
    if user_id not in users or message.text == '/language':
        # Send a welcome message and ask the user to choose a language
        language_keyboard = telebot.types.InlineKeyboardMarkup()
        for lang in languages:
            language_keyboard.add(
                telebot.types.InlineKeyboardButton(lang, callback_data=lang))
        bot.send_message(user_id, "Choose Your language:",
                         reply_markup=language_keyboard)
    else:
        user_language = users[user_id]['language']
        greeting = languages[user_language]['greeting']
        instructions = languages[user_language]['instructions']

        # Create inline keyboard
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(telebot.types.InlineKeyboardButton(
            "➕ Add Your Group ➕", url="https://t.me/JoinHiderGTIBot?startgroup=inpvbtn")),

        keyboard.add(
            telebot.types.InlineKeyboardButton(
                "👥 Group", url="https://t.me/GettechinfoGroup"),
            telebot.types.InlineKeyboardButton("📢 Channel", url="https://t.me/Gettechinfo1st"), row_width=2)

        keyboard.add(telebot.types.InlineKeyboardButton(
            "😒 Developer", url="https://t.me/MilesTM")),

        bot.reply_to(
            message, f"{greeting} {instructions}", reply_markup=keyboard)

        bot.delete_message(chat_id, message_id)


# Define the language selection callback
@bot.callback_query_handler(func=lambda call: call.data in languages)
def language_callback_handler(call):
    user_id = call.message.chat.id
    user_language = call.data
    users[user_id] = {'language': user_language}
    bot.answer_callback_query(
        call.id, text=languages[user_language]['language_set'])
    # Remove the language selection inline keyboard
    bot.edit_message_reply_markup(
        chat_id=user_id, message_id=call.message.message_id, reply_markup=None)
    # Go back to the start handler
    language_handler(call.message)


# Start the bot
print("I am up")
bot.polling()
