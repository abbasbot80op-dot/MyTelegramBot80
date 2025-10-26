import telebot
from telebot import types
from flask import Flask, send_from_directory
import threading
import os

# 🔑 ضع التوكن الخاص بك هنا
TOKEN = "8248283131:AAH5LG0OFxH4pgTxwU1xuN_gE8I967gP-sE"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ✅ عرض صفحة المتجر index.html
@app.route('/')
def serve_store():
    return send_from_directory('.', 'index.html')

# ✅ بوت تيليجرام
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    webApp = types.WebAppInfo("https://77fb188c-2591-4f7c-9908-3c45b7b63a7e-00-1mz48ec8cqou7.pike.replit.dev")  # 👈 غيّر هذا إلى رابط موقعك على Render
    btn = types.InlineKeyboardButton(text="🛒 فتح المتجر", web_app=webApp)
    markup.add(btn)
    bot.send_message(message.chat.id, "مرحبًا بك في متجر سنو 🛍️", reply_markup=markup)

# ✅ تشغيل البوت بشكل دائم
def run_bot():
    bot.polling(non_stop=True, interval=0, timeout=20)

# ✅ تشغيل Flask (لصفحة الويب)
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    t1 = threading.Thread(target=run_bot)
    t2 = threading.Thread(target=run_flask)
    t1.start()
    t2.start()
