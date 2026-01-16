from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8316089455:AAGfVqlJYcSgqIJJ8rX-rOh_7YIh7NyVIL4"

users = {}        # user_id: {"name": str, "state": str}
tests = {}        # code: answer
answered = {}     # code: set(user_id)

keyboard = ReplyKeyboardMarkup(
    [["🆕 Yangi test yaratish"], ["📝 Testga javob berish"]],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    users[user_id] = {"state": "name"}
    await update.message.reply_text(
        "📝 Ism va familiyangizni kiriting.\nLotin harflaridan foydalaning."
    )

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip().lower()

    if user_id not in users:
        await update.message.reply_text("❗ Iltimos /start buyrug‘ini bosing.")
        return

    state = users[user_id]["state"]

    # 1️⃣ Ism kiritish
    if state == "name":
        users[user_id]["name"] = text
        users[user_id]["state"] = "menu"
        await update.message.reply_text(
            "✅ Ma'lumot saqlandi.\nBo‘limni tanlang 👇",
            reply_markup=keyboard
        )
        return

    # 2️⃣ Tugmalar
    if text == "🆕 yangi test yaratish":
        await update.message.reply_text(
            "Test nomi + kalitlarni kiriting\n\n"
            "Misol:\nMatematika+abcdabcd"
        )
        return

    if text == "📝 testga javob berish":
        users[user_id]["state"] = "answer"
        await update.message.reply_text(
            "Test kodi * javob\n\n"
            "Misol:\n101*abcdabcd"
        )
        return

    # 3️⃣ Test yaratish
    if "+" in text:
        name, answer = text.split("+", 1)
        code = str(len(tests) + 100)
        tests[code] = answer
        answered[code] = set()

        await update.message.reply_text(
            f"✅ Test yaratildi!\n"
            f"🆔 Kod: {code}\n"
            f"📏 Savollar soni: {len(answer)} ta"
        )
        return

    # 4️⃣ Testga javob
    if state == "answer" and "*" in text:
        code, user_answer = text.split("*", 1)

        if code not in tests:
            await update.message.reply_text("❌ Test topilmadi.")
            return

        correct = tests[code]
        total = len(correct)

        # 🔹 OLDINDAN nechta savol ekanini aytish
        if len(user_answer) != total:
            await update.message.reply_text(
                f"⚠️ Bu test {total} ta savoldan iborat.\n"
                f"Javob uzunligi mos emas."
            )
            return

        if user_id in answered[code]:
            await update.message.reply_text("⚠️ Siz bu testga javob bergansiz.")
            return

        true_count = 0
        false_count = 0

        for u, c in zip(user_answer, correct):
            if u == c:
                true_count += 1
            else:
                false_count += 1

        percent = round((true_count / total) * 100, 2)
        answered[code].add(user_id)

        await update.message.reply_text(
            f"📊 NATIJA:\n\n"
            f"✅ To‘g‘ri: {true_count}\n"
            f"❌ Xato: {false_count}\n"
            f"📏 Jami: {total}\n"
            f"🎯 Foiz: {percent}%"
        )
        return

    await update.message.reply_text("❗ Buyruq noto‘g‘ri.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    print("🤖 Bot ishga tushdi")
    app.run_polling()

if __name__ == "__main__":
    main()



