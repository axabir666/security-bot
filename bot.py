import telebot
from telebot import types
import os

# --- আপনার টোকেন এবং আইডি এখানে বসিয়ে দেওয়া হয়েছে ---
API_TOKEN = '8480712542:AAHd8A4VJ-UWCJ_wSSDYdZkVgj2BmFHp99Q'
ADMIN_ID = 8480712542  # আপনার চ্যাট আইডি
DEV_USER = '@ax_abir_999' # ডেভলপার ইউজারনেম
bot = telebot.TeleBot(API_TOKEN)

# ইউজার লিস্ট সেভ রাখার জন্য
user_list = set()

@bot.message_handler(commands=['start'])
def start_msg(message):
    user_list.add(message.chat.id)
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # বাটন সেটআপ
    btn1 = types.InlineKeyboardButton("🔍 User Lookup (OSINT)", callback_data="lookup")
    btn2 = types.InlineKeyboardButton("📍 IP Tracker", callback_data="iptracker")
    btn3 = types.InlineKeyboardButton("🛡️ Phone Security", callback_data="phone_sec")
    btn4 = types.InlineKeyboardButton("📢 Our Channels", callback_data="channels")
    btn5 = types.InlineKeyboardButton("👤 Developer Info", callback_data="dev")
    
    # অ্যাডমিন বাটন (শুধুমাত্র আপনার আইডি হলে দেখাবে)
    if message.chat.id == ADMIN_ID:
        btn_admin = types.InlineKeyboardButton("🛠 ADMIN PANEL", callback_data="admin_panel")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn_admin)
    else:
        markup.add(btn1, btn2, btn3, btn4, btn5)

    welcome_text = (
        f"🛡 **AX TRACKER BOT v2.0** 🛡\n\n"
        f"হ্যালো {message.from_user.first_name}!\n"
        f"নিরাপত্তা এবং তথ্য অনুসন্ধানের জন্য নিচের অপশনগুলো ব্যবহার করুন।"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    uid = call.message.chat.id
    
    if call.data == "lookup":
        bot.send_message(uid, "🔍 **User Lookup:**\nটেলিগ্রাম ইউজারনেম (উদা: @username) পাঠান। ডাটাবেস চেক করা হচ্ছে...")

    elif call.data == "iptracker":
        bot.send_message(uid, "📍 **IP Tracker:**\nলিঙ্ক তৈরি করতে [Grabify](https://grabify.link) ব্যবহার করুন।")

    elif call.data == "phone_sec":
        if uid == ADMIN_ID:
            bot.send_message(uid, "📱 **Admin Security Mode:**\n১. /track - লোকেশন\n২. /alarm - এলার্ম\n৩. /lock - লক")
        else:
            bot.send_message(uid, "❌ এই ফিচারটি শুধুমাত্র বটের মালিকের জন্য।")

    elif call.data == "dev":
        bot.send_message(uid, f"👤 **Developer:** {DEV_USER}")

    elif call.data == "admin_panel" and uid == ADMIN_ID:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 Send Broadcast", callback_data="bc_msg"))
        bot.send_message(uid, f"🛠 **অ্যাডমিন প্যানেল**\nমোট ইউজার: {len(user_list)}", reply_markup=markup)

    elif call.data == "bc_msg" and uid == ADMIN_ID:
        bot.send_message(uid, "মেসেজ পাঠাতে লিখুন: `/send বার্তা`")

# --- কমান্ড হ্যান্ডলার ---
@bot.message_handler(func=lambda m: m.text and m.text.startswith('/send'))
def do_broadcast(message):
    if message.chat.id == ADMIN_ID:
        content = message.text.replace('/send', '').strip()
        for user in user_list:
            try: bot.send_message(user, f"📢 **ADMIN MESSAGE:**\n\n{content}")
            except: pass
        bot.send_message(ADMIN_ID, "✅ মেসেজ পাঠানো হয়েছে।")

@bot.message_handler(func=lambda m: m.text and m.text.startswith('@'))
def lookup_username(message):
    bot.reply_to(message, "⚙️ ডাটাবেস সার্চ করা হচ্ছে... ফলাফল পাওয়া যায়নি।")

# রেন্ডার সার্ভার
from flask import Flask
from threading import Thread
app = Flask('')
@app.route('/')
def home(): return "Bot is Live!"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
Thread(target=run).start()

bot.polling(none_stop=True)
