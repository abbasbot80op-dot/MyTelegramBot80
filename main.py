import os
import time
import telebot
from telebot import types
from flask import Flask
from threading import Thread

# قراءة التوكن من Render
TOKEN = os.environ.get("TOKEN")

if not TOKEN:
    raise Exception("❌ Bot token is not defined. Please set TOKEN in Render Environment.")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# صفحة Render الرئيسية
@app.route('/')
def home():
    return "✅ Snow Store Bot is Running Successfully!"

# أمر /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    webApp = types.WebAppInfo("https://77fb188c-2591-4f7c-9908-3c45b7b63a7e-00-1mz48ec8cqou7.pike.replit.dev")
    btn = types.InlineKeyboardButton(text="🛒 فتح المتجر", web_app=webApp)
    markup.add(btn)
    bot.send_message(message.chat.id, "مرحبًا بك في متجر سنو ❄️\nاضغط الزر بالأسفل لفتح المتجر:", reply_markup=markup)

# تشغيل Flask
def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

# تشغيل البوت بثبات
def run_bot():
    while True:
        try:
            print("🚀 Bot started polling...")
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"⚠️ Bot crashed with error: {e}")
            print("🔁 Restarting bot in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    run_bot()
