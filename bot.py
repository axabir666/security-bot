import telebot
from telebot import types
import os

# --- সঠিক কনফিগারেশন ---
API_TOKEN = '7867771491:AAFrYzFOeDRnSiH2FaqND3Pr3TtQj9aDFOI'
ADMIN_ID = 8293410345  # এখানে কোনো কোটেশন থাকবে না
DEV_USER = '@ax_abir_999'
CHANNEL_LINK = 'https://t.me/ax_abir_999'

bot = telebot.TeleBot(API_TOKEN, parse_mode="Markdown")
user_list = set()

@bot.message_handler(commands=['start'])
def start_msg(message):
    user_list.add(message.chat.id)
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("🔍 USER LOOKUP (OSINT)", callback_data="lookup")
    btn2 = types.InlineKeyboardButton("📍 IP TRACKER", callback_data="iptracker")
    btn3 = types.InlineKeyboardButton("🛡️ PHONE SECURITY", callback_data="phone_sec")
    btn4 = types.InlineKeyboardButton("📢 OUR CHANNEL", url=CHANNEL_LINK)
    btn5 = types.InlineKeyboardButton("👤 DEVELOPER", callback_data="dev")
    
    if message.chat.id == ADMIN_ID:
        btn_admin = types.InlineKeyboardButton("🛠 ADMIN PANEL (PRIVATE)", callback_data="admin_panel")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn_admin)
    else:
        markup.add(btn1, btn2, btn3, btn4, btn5)

    welcome_text = f"🛡 **AX TRACKER BOT v3.0** 🛡\n\n**হ্যালো {message.from_user.first_name}!**\n**আমাদের প্রিমিয়াম বোর্ডে আপনাকে স্বাগতম।**"
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    uid = call.message.chat.id
    if call.data == "lookup":
        bot.send_message(uid, "**🔍 ইউজারনেম পাঠান। সিস্টেম ডাটাবেস চেক করছে...**")
    elif call.data == "iptracker":
        bot.send_message(uid, "**📍 আইপি ট্র্যাকিং লিংক তৈরি করতে Grabify ব্যবহার করুন।**")
    elif call.data == "phone_sec":
        if uid == ADMIN_ID:
            bot.send_message(uid, "**📱 কমান্ডস: /track, /alarm, /lock**")
        else:
            bot.send_message(uid, "**❌ এই ফিচারটি শুধুমাত্র অ্যাডমিনের জন্য।**")
    elif call.data == "dev":
        bot.send_message(uid, f"**👤 DEVELOPER:** {DEV_USER}")

from flask import Flask
from threading import Thread
app = Flask('')
@app.route('/')
def home(): return "Online"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
Thread(target=run).start()
bot.polling(none_stop=True)
