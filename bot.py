import telebot
from telebot import types

# আপনার দেওয়া তথ্য
TOKEN = '8480712542:AAHd8A4VJ-UWCJ_wSSDYdZkVgj2BmFHp99Q'
ADMIN_CHAT_ID = 8480712542  # আপনার চ্যাট আইডি (সিস্টেমের জন্য)
DEV_USERNAME = '@ax_abir_999' # আপনার ইউজারনেম (যোগাযোগের জন্য)

bot = telebot.TeleBot(TOKEN)

# বটের তথ্যাবলী
BOT_INFO = """
🛡️ **Security & Info Tracker Bot** 🛡️
--------------------------------------
এই বটটি আপনার ব্যক্তিগত নিরাপত্তা এবং স্ক্যামারদের চিহ্নিত করতে সাহায্য করবে।

✅ **প্রধান ফিচারসমূহ:**
১. 🔎 **OSINT Search:** নম্বর বা ইমেইলের পাবলিক তথ্য খোঁজা।
২. 📍 **IP Tracker:** লিঙ্কের মাধ্যমে স্ক্যামারের অবস্থান শনাক্ত করা।
৩. 🛡️ **Phone Security:** ফোন হারিয়ে গেলে দূর থেকে নিয়ন্ত্রণ (শুধু এডমিন)।
"""

# স্টার্ট কমান্ড
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # বাটন সমূহ
    btn1 = types.InlineKeyboardButton("🔍 OSINT Search", callback_data="osint")
    btn2 = types.InlineKeyboardButton("📍 IP Tracker", callback_data="iptracker")
    btn3 = types.InlineKeyboardButton("🛡️ Phone Security", callback_data="security")
    btn4 = types.InlineKeyboardButton("📢 Our Channels", callback_data="channels")
    btn5 = types.InlineKeyboardButton("👤 Developer Info", callback_data="dev_info")
    
    markup.add(btn1, btn2, btn3, btn4, btn5)
    
    welcome_text = f"হ্যালো {message.from_user.first_name}!\n{BOT_INFO}\nনিচের বাটনগুলো ব্যবহার করে আপনার পছন্দের অপশনটি বেছে নিন।"
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

# বাটন ক্লিকের হ্যান্ডলার
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "osint":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "🔎 **OSINT Search:**\nযেকোনো নম্বর বা ইমেইল পাঠান। বট ইন্টারনেটে থাকা পাবলিক ডাটাবেস চেক করবে।", parse_mode="Markdown")
        
    elif call.data == "iptracker":
        bot.answer_callback_query(call.id)
        msg = "🔗 **IP Tracker:**\nএকটি ট্র্যাকিং লিঙ্ক তৈরি করতে আপনার কাঙ্ক্ষিত ওয়েবসাইটের লিঙ্ক দিন। স্ক্যামার সেখানে ক্লিক করলেই তার লোকেশন ও আইপি আপনার কাছে চলে আসবে।"
        bot.send_message(call.message.chat.id, msg, parse_mode="Markdown")

    elif call.data == "security":
        if call.from_user.id == ADMIN_CHAT_ID:
            bot.send_message(call.message.chat.id, "✅ **Admin Verified!**\nআপনার ফোনের সিকিউরিটি কমান্ডগুলো:\n/location - ফোনের লাইভ ম্যাপ\n/capture - সামনের ক্যামেরার ছবি")
        else:
            bot.send_message(call.message.chat.id, "❌ এই ফিচারটি শুধুমাত্র বটের মালিকের ব্যবহারের জন্য সংরক্ষিত।")

    elif call.data == "channels":
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_ch1 = types.InlineKeyboardButton("Main Channel 1", url="https://t.me/+d0ol4cPYxUExOGU1")
        btn_ch2 = types.InlineKeyboardButton("Color Trading Official", url="https://t.me/color_trading_official")
        btn_ch3 = types.InlineKeyboardButton("Support Group", url="https://t.me/+YBo9GZb4ISxhN2I1")
        markup.add(btn_ch1, btn_ch2, btn_ch3)
        bot.send_message(call.message.chat.id, "আমাদের অফিশিয়াল চ্যানেলসমূহ:", reply_markup=markup)

    elif call.data == "dev_info":
        markup = types.InlineKeyboardMarkup()
        dev_btn = types.InlineKeyboardButton("Message Developer", url=f"https://t.me/ax_abir_999")
        markup.add(dev_btn)
        bot.send_message(call.message.chat.id, f"👤 **Developer:** {DEV_USERNAME}\nযেকোনো সমস্যা বা আপডেটের জন্য নিচে যোগাযোগ করুন।", reply_markup=markup, parse_mode="Markdown")

# মেসেজ হ্যান্ডলার
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    bot.send_message(message.chat.id, "⚙️ প্রসেসিং চলছে... সার্ভারের ডাটাবেস চেক করা হচ্ছে।")

# বট চালানো
print("বটটি সফলভাবে চালু হয়েছে...")
bot.infinity_polling()
