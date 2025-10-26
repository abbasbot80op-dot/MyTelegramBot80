import os
import threading
import logging
from flask import Flask, send_from_directory
try:
    import telebot
    from telebot import types
except Exception:
    telebot = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("botapp")

# اقرأ التوكن من متغير البيئة
TOKEN = os.environ.get("TOKEN")

app = Flask(name)

@app.route('/')
def serve_store():
    return send_from_directory('.', 'index.html')

# دالة لإعداد وتشغيل البوت فقط إذا كانت المكتبة والتوكن متوفرين
def run_bot_safe():
    if telebot is None:
        logger.error("pyTelegramBotAPI غير مثبت. تأكد من requirements.txt")
        return
    if not TOKEN:
        logger.warning("متغير البيئة TOKEN غير موجود — البوت لن يبدأ. أضف TOKEN في إعدادات Render.")
        return

    bot = telebot.TeleBot(TOKEN)

    @bot.message_handler(commands=['start'])
    def start(message):
        markup = types.InlineKeyboardMarkup()
        # ضع رابط موقعك هنا بعد نشره على Render
        webApp = types.WebAppInfo("https://77fb188c-2591-4f7c-9908-3c45b7b63a7e-00-1mz48ec8cqou7.pike.replit.dev")
        btn = types.InlineKeyboardButton(text="🛒 فتح المتجر", web_app=webApp)
        markup.add(btn)
        bot.send_message(message.chat.id, "مرحبًا بك في متجر سنو 🛍️", reply_markup=markup)

    try:
        logger.info("بدء تشغيل TeleBot polling ...")
        bot.polling(non_stop=True, interval=0, timeout=20)
    except Exception as e:
        logger.exception("حدث خطأ أثناء تشغيل البوت: %s", e)

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    logger.info("تشغيل Flask على المنفذ %s", port)
    app.run(host="0.0.0.0", port=port)

if name == "main":
    # شغّل Flask دائماً، وشغّل البوت فقط إن كانت الشروط متوفرة
    t1 = threading.Thread(target=run_flask)
    t1.start()

    # شغّل البوت في خيط منفصل (سيقوم بالكشف داخلياً إذا لم يبدأ)
    t2 = threading.Thread(target=run_bot_safe)
    t2.start()
