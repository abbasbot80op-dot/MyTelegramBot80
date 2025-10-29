import os
import telebot
from telebot import types

TOKEN = os.environ.get("TOKEN")
WEBAPP_URL = os.environ.get("WEBAPP_URL")  # رابط صفحتك (index.html)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user

    # بيانات المستخدم
    name = (user.first_name or "") + " " + (user.last_name or "")
    username = user.username or "Guest"
    photo_url = ""

    # نحاول جلب صورة المستخدم
    try:
        photos = bot.get_user_profile_photos(user.id, limit=1)
        if photos.total_count > 0:
            file_id = photos.photos[0][0].file_id
            file_info = bot.get_file(file_id)
            photo_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"
    except:
        pass

    # نبني رابط الصفحة مع البيانات
    web_link = f"{WEBAPP_URL}?name={name}&username={username}&photo={photo_url}"

    # زر فتح المتجر
    markup = types.InlineKeyboardMarkup()
    webApp = types.WebAppInfo(web_link)
    btn = types.InlineKeyboardButton(text="❄️ افتح متجر Snow Store", web_app=webApp)
    markup.add(btn)

    bot.send_message(
        message.chat.id,
        "مرحبًا بك في متجر سنو ❄️\nاضغط الزر بالأسفل لفتح المتجر:",
        reply_markup=markup
    )

print("✅ Bot is running...")
bot.infinity_polling()
