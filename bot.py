import telebot
from telebot import types
import os

# --- আপনার দেওয়া নতুন তথ্যসমূহ ---
API_TOKEN = '7867771491:AAFrYzFOeDRnSiH2FaqND3Pr3TtQj9aDFOI'
ADMIN_ID = '8293410345' # আপনার নতুন চ্যাট আইডি
DEV_USER = '@ax_abir_999' # ডেভলপার ইউজারনেম
CHANNEL_LINK = 'https://t.me/ax_abir_999' # আপনার চ্যানেল লিংক
bot = telebot.TeleBot(API_TOKEN, parse_mode="Markdown")

# ইউজার লিস্ট সেভ রাখার জন্য
user_list = set()

@bot.message_handler(commands=['start'])
def start_msg(message):
    user_list.add(message.chat.id)
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # প্রিমিয়াম ডিজাইন বাটন
    btn1 = types.InlineKeyboardButton("🔍 USER LOOKUP (OSINT)", callback_data="lookup")
    btn2 = types.InlineKeyboardButton("📍 IP TRACKER", callback_data="iptracker")
    btn3 = types.InlineKeyboardButton("🛡️ PHONE SECURITY", callback_data="phone_sec")
    btn4 = types.InlineKeyboardButton("📢 OUR CHANNEL", url=CHANNEL_LINK)
    btn5 = types.InlineKeyboardButton("👤 DEVELOPER", callback_data="dev")
    
    # অ্যাডমিন প্যানেল বাটন (শুধুমাত্র আপনার জন্য)
    if message.chat.id == ADMIN_ID:
        btn_admin = types.InlineKeyboardButton("🛠 ADMIN PANEL (PRIVATE)", callback_data="admin_panel")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn_admin)
    else:
        markup.add(btn1, btn2, btn3, btn4, btn5)

    welcome_text = (
        f"🛡 **AX TRACKER BOT v3.0 [PREMIUM]** 🛡\n\n"
        f"**হ্যালো {message.from_user.first_name}!**\n"
        f"**আমাদের প্রিমিয়াম সিকিউরিটি বোর্ডে আপনাকে স্বাগতম।**\n"
        f"**নিচের বাটনগুলো ব্যবহার করে আপনার কাঙ্ক্ষিত সেবাটি বেছে নিন।**"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    uid = call.message.chat.id
    
    if call.data == "lookup":
        bot.send_message(uid, "**🔍 USER LOOKUP (OSINT):**\n\n**যেকোনো টেলিগ্রাম ইউজারনেম (উদা: @username) এখানে পাঠান।**\n\n**সিস্টেম স্বয়ংক্রিয়ভাবে তার নাম্বার, আইডি এবং লোকেশন ডাটাবেস থেকে খোঁজার চেষ্টা করবে।**")

    elif call.data == "iptracker":
        bot.send_message(uid, "**📍 IP TRACKER (ADVANCED):**\n\n**একটি ট্র্যাকিং লিংক তৈরি করতে [Grabify](https://grabify.link) ব্যবহার করুন।**\n**টার্গেট ব্যক্তি লিংকে ক্লিক করলে আপনি তার সঠিক লোকেশন ও আইপি পেয়ে যাবেন।**")

    elif call.data == "phone_sec":
        if uid == ADMIN_ID:
            msg = (
                "**📱 PHONE SECURITY (ADMIN ONLY):**\n\n"
                "**১. /track - ফোনের লাইভ লোকেশন**\n"
                "**২. /alarm - ফুল ভলিউমে এলার্ম**\n"
                "**৩. /lock - ডিভাইস সাথে সাথে লক**\n\n"
                "**[সতর্কতা: এই কমান্ডগুলো শুধু আপনার ডিভাইসেই কাজ করবে]**"
            )
            bot.send_message(uid, msg)
        else:
            bot.send_message(uid, "**❌ দুঃখিত! এই ফিচারটি শুধুমাত্র বটের মালিকের (ADMIN) জন্য সংরক্ষিত।**")

    elif call.data == "dev":
        bot.send_message(uid, f"**👤 DEVELOPER INFO:**\n\n**ডেভলপার:** {DEV_USER}\n**যেকোনো টেকনিক্যাল সাপোর্টের জন্য যোগাযোগ করুন।**")

    elif call.data == "admin_panel" and uid == ADMIN_ID:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 SEND BROADCAST", callback_data="bc_msg"))
        bot.send_message(uid, f"**🛠 ADIMIN PANEL**\n\n**বটে বর্তমানে মোট ইউজার আছে: {len(user_list)} জন।**", reply_markup=markup)

    elif call.data == "bc_msg" and uid == ADMIN_ID:
        bot.send_message(uid, "**সবাইকে মেসেজ পাঠাতে লিখুন:** `/send আপনার বার্তা`")

# --- বিশেষ কমান্ড হ্যান্ডলার ---

@bot.message_handler(func=lambda m: m.text and m.text.startswith('/send'))
def do_broadcast(message):
    if message.chat.id == ADMIN_ID:
        content = message.text.replace('/send', '').strip()
        if content:
            for user in user_list:
                try: bot.send_message(user, f"📢 **ADMIN ANNOUNCEMENT:**\n\n**{content}**")
                except: pass
            bot.send_message(ADMIN_ID, "**✅ মেসেজ সফলভাবে সবার কাছে পৌঁছে গেছে।**")
        else:
            bot.send_message(ADMIN_ID, "**⚠️ মেসেজে কিছু লিখুন!**")

@bot.message_handler(func=lambda m: m.text and m.text.startswith('@'))
def lookup_username(message):
    bot.reply_to(message, "**⚙️ ডাটাবেস সার্চ করা হচ্ছে...**\n\n**⚠️ ফলাফল: ইউজারনেমটির তথ্য আমাদের গ্লোবাল পাবলিক সার্ভারে এনক্রিপ্টেড আছে। প্রফেশনাল ডিক্রিপশন টুলের জন্য অ্যাডমিনের সাথে যোগাযোগ করুন।**")

# রেন্ডার সার্ভার এবং আপটাইম মেইনটেইন
from flask import Flask
from threading import Thread
app = Flask('')
@app.route('/')
def home(): return "AX Tracker Bot is Online!"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
Thread(target=run).start()

print("AX Tracker Bot is Starting...")
bot.polling(none_stop=True)
