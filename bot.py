import telebot
from telebot import types
import time
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "1977278560:AAHh1qUVcBElc4cFA5BSNQY0FvGpKzcgwrg"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):

    bot.send_chat_action(message.chat.id, 'typing')
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton(
            "😉 Add Your Group", url="https://t.me/JoinHiderGTIBot?startgroup=inpvbtn"),
        InlineKeyboardButton("😒 MyFather", url="https://t.me/MilesTM"))
    markup.add(
        InlineKeyboardButton(
            "☺️ Our YT Channel", url="https://www.youtube.com/c/Gettechinfo?sub_confirmation=1"),
        InlineKeyboardButton("🙄 Support", url="https://t.me/GettechinfoGroup"))

    bot.send_message(chat_id=message.chat.id, text=u' 😌 Hi! ' + message.from_user.first_name +
                     '\n\n I am your trusty GroupSilencer Bot! \n\n🥰Thanks for Choosing me!\n\nTo use me, make me an admin and I will be able to delete all the pesky notification when a member joins or leaves the group! \n\n እኔን ለመጠቀም አስተዳዳሪ አድርገኝ እና አንድ አባል ከቡድኑ ሲቀላቀል ወይም ሲወጣ ሁሉንም ማስታወቂያዎች መሰረዝ እችላለሁ! \n\n😋 Please add me to your groups\n እባክዎን ወደ ቡድኖችዎ  ያስገቡኝ  \n\n', reply_markup=markup)


@bot.message_handler(content_types=['new_chat_members'])
def delete_join_message(m):
    # If bot is not admin, then it will not be able to delete message.
    try:
        bot.delete_message(m.chat.id, m.message_id)
    except:
        if m.new_chat_member.id != bot.get_me().id:
            bot.send_message(
                m.chat.id, "Please make me an admin in order for me to remove the join and leave messages on this group!")
        else:
            bot.send_message(m.chat.id, "")


@bot.message_handler(content_types=['left_chat_member'])
def delete_leave_message(m):
    # If bot is the one that is being removed, it will not be able to delete the leave message.
    if m.left_chat_member.id != bot.get_me().id:
        try:
            bot.delete_message(m.chat.id, m.message_id)
        except:
            bot.send_message(
                m.chat.id, "Please make me an admin in order for me to remove the join and leave messages on this group!")


bot.polling()
