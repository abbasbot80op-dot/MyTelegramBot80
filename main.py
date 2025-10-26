import os
import telebot
from telebot import types
from flask import Flask

# قراءة التوكن من بيئة Render (تأكد أنك أضفت TOKEN هناك)
TOKEN = os.environ.get("TOKEN")

bot = telebot.TeleBot(TOKEN)

# إنشاء تطبيق Flask ليبقى البوت نشطًا دائمًا
app = Flask(__name__)

# مسار افتراضي للموقع
@app.route('/')
def home():
    return "✅ Snow Store Bot is Running Successfully!"

# أمر /start في البوت
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    webApp = types.WebAppInfo("https://77fb188c-2591-4f7c-9908-3c45b7b63a7e-00-1mz48ec8cqou7.pike.replit.dev")
    btn = types.InlineKeyboardButton(text="🛒 فتح المتجر", web_app=webApp)
    markup.add(btn)
    bot.send_message(message.chat.id, "مرحبًا بك في متجر سنو ❄️\nاضغط الزر بالأسفل لفتح المتجر:", reply_markup=markup)

# لتشغيل البوت بشكل دائم
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    from threading import Thread

    # تشغيل Flask على منفذ Render
    Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))).start()
    run_bot()
