import os
import telebot
from telebot import types

TOKEN = os.environ.get("TOKEN")
WEBAPP_URL = os.environ.get("WEBAPP_URL")  # رابط صفحتك (index.html)

if not TOKEN or not WEBAPP_URL:
    raise Exception("❌ تأكد من أنك أضفت TOKEN و WEBAPP_URL في إعدادات Render")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    webApp = types.WebAppInfo(WEBAPP_URL)
    btn = types.InlineKeyboardButton(text="❄️ افتح متجر Snow Store", web_app=webApp)
    markup.add(btn)
    bot.send_message(
        message.chat.id,
        "مرحبًا بك في متجر سنو ❄️\nاضغط الزر بالأسفل لفتح المتجر:",
        reply_markup=markup
    )

print("✅ Bot is running...")
bot.infinity_polling()
