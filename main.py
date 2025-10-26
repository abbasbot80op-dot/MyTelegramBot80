import telebot
from telebot import types

TOKEN = "8248283131:AAH5LG0OFxH4pgTxwU1xuN_gE8I967gP-sE"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    webApp = types.WebAppInfo("https://77fb188c-2591-4f7c-9908-3c45b7b63a7e-00-1mz48ec8cqou7.pike.replit.dev")
    btn = types.InlineKeyboardButton(text="🛒 فتح المتجر", web_app=webApp)
    markup.add(btn)
    bot.send_message(message.chat.id, "مرحبًا بك في متجر سنو 🛍️", reply_markup=markup)

bot.polling()