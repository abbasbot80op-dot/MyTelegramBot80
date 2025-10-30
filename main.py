import os
from flask import Flask, request, send_from_directory, redirect
import telebot

TOKEN = os.environ.get("TOKEN")
WEBAPP_URL = os.environ.get("WEBAPP_URL")  # مثال: https://weptelegrame.onrender.com

if not TOKEN:
    raise Exception("⚠️ لم يتم العثور على TOKEN في المتغيرات البيئية")
if not WEBAPP_URL:
    raise Exception("⚠️ تأكد من إعداد WEBAPP_URL (رابط موقعك العام) في Environment variables")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__, static_folder='static', static_url_path='')

# ---------- خدمة صفحات الويب ----------
# إذا وضعت index.html في نفس الجذر (أو في مجلد static) يمكنك تعديله حسب مكانه.
@app.route("/", methods=["GET"])
def index():
    # Serve index.html from project root or static folder
    # إذا وضعت index.html في نفس مجلد المشروع:
    if os.path.exists("index.html"):
        return send_from_directory('.', "index.html")
    # أو من مجلد static:
    return send_from_directory('static', "index.html")

# مسار اختياري إذا أردت استقبال event من Telegram (webhook)
@app.route("/webhook", methods=["POST"])
def webhook():
    # تمرير الطلب لكتلة telebot لمعالجة التحديث من تلغرام
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "OK", 200

# ---------- رسائل / اوامر البوت ----------
@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user

    # اسم ويوزر
    name = (user.first_name or "") + (" " + user.last_name if user.last_name else "")
    username = user.username or ""

    # نحاول جلب صورة ملف المستخدم (رابط مباشر الى ملف بوت)
    photo_url = ""
    try:
        photos = bot.get_user_profile_photos(user.id, limit=1)
        if photos.total_count > 0:
            file_id = photos.photos[0][0].file_id
            file_info = bot.get_file(file_id)
            photo_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"
    except Exception:
        photo_url = ""

    # طريقة 1: نفتح Web App مباشرة (أفضل داخل Telegram)
    # نمرّر البيانات كـ query params احتياطيًا (ستُستخدم إن لزم)
    import urllib.parse
    params = {
        "name": name,
        "username": username,
        "photo": photo_url
    }
    web_link = WEBAPP_URL + "?" + urllib.parse.urlencode(params)

    markup = telebot.types.InlineKeyboardMarkup()
    webApp = telebot.types.WebAppInfo(WEBAPP_URL)  # ضع LINK فقط (Telegram يزود بيانات داخل WebApp)
    btn = telebot.types.InlineKeyboardButton(text="❄️ افتح متجر Snow Store", web_app=webApp)
    markup.add(btn)

    bot.send_message(
        message.chat.id,
        "مرحبًا بك في متجر سنو ❄️\nاضغط الزر بالأسفل لفتح المتجر داخل Telegram:",
        reply_markup=markup
    )

# ---------- تهيئة webhook (مهم) ----------
def set_webhook():
    # يضع البوت webhook إلى عنوان /webhook في موقعك
    webhook_url = WEBAPP_URL.rstrip("/") + "/webhook"
    bot.remove_webhook()
    s = bot.set_webhook(webhook_url)
    print("set_webhook:", s, "->", webhook_url)

# عندما يتم تشغيل التطبيق تحت Gunicorn، استدعاء set_webhook مرة واحدة
if __name__ == "__main__":
    set_webhook()
    print("Bot polling fallback (not used on Render).")
    bot.infinity_polling()
else:
    # Gunicorn سيستورد هذا الملف ك module و سيستخدم app كـ WSGI callable
    # نضبط ال webhook عند الاستيراد (startup)
    try:
        set_webhook()
    except Exception as e:
        print("Webhook setup error:", e)
