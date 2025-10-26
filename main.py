import os
import threading
import telebot
from telebot import types
from flask import Flask, send_from_directory

# TOKEN لا تضعه هنا؛ سيتم وضعه كمتغير بيئة على Render
TOKEN = os.environ.get("TOKEN")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# سيرفر لعرض index.html من نفس مجلد المشروع
@app.route('/')
def serve_store():
    return send_from_directory('.', 'index.html')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    # استبدل هذا بالرابط النهائي لموقعك على Render لاحقًا
    webApp = types.WebAppInfo("https://your-render-url.onrender.com")
    btn = types.InlineKeyboardButton(text="🛒 فتح المتجر", web_app=webApp)
    markup.add(btn)
    bot.send_message(message.chat.id, "مرحبًا بك في متجر سنو 🛍️", reply_markup=markup)

def run_bot():
    # non_stop=True يحاول إعادة الاتصال تلقائيًا
    bot.polling(non_stop=True, interval=0, timeout=20)

def run_flask():
    # Render يعطي المنفذ في متغير البيئة PORT — استخدمه
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    t1 = threading.Thread(target=run_bot)
    t2 = threading.Thread(target=run_flask)
    t1.start()
    t2.start()
