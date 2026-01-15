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
        "📝 Ism va familiyangizni kiriting.\n"
        "Lotin harflaridan foydalaning."
    )

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip()

    if user_id not in users:
        await update.message.reply_text("❗ Iltimos /start buyrug‘ini bosing.")
        return

    state = users[user_id]["state"]

    # 1️⃣ Ism kiritish
    if state == "name":
        users[user_id]["name"] = text
        users[user_id]["state"] = "menu"
        await update.message.reply_text(
            "✅ Ma'lumot saqlandi.\n\nBo‘limni tanlang 👇",
            reply_markup=keyboard
        )
        return

    # 2️⃣ Tugmalar
    if text == "🆕 Yangi test yaratish":
        await update.message.reply_text(
            "Test nomi + kalitlarni kiriting\n\n"
            "Misol:\nMatematika+abcdabcd"
        )
        return

    if text == "📝 Testga javob berish":
        await update.message.reply_text(
            "Test kodi * javob\n\n"
            "Misol:\n101*abcdabcd"
        )
        return

    # 3️⃣ Test yaratish
    if "+" in text:
        name, answer = text.split("+", 1)
        code = str(len(tests) + 100)
        tests[code] = answer.lower()
        answered[code] = set()
        await update.message.reply_text(
            f"✅ Test yaratildi!\n🆔 Kod: {code}"
        )
        return

    # 4️⃣ Testga javob
    if "*" in text:
        code, user_answer = text.split("*", 1)
        user_answer = user_answer.lower()

        if code not in tests:
            await update.message.reply_text("❌ Test topilmadi.")
            return

        if user_id in answered[code]:
            await update.message.reply_text("⚠️ Siz bu testga javob bergansiz.")
            return

        answered[code].add(user_id)

        if user_answer == tests[code]:
            await update.message.reply_text("🎉 To‘g‘ri!")
        else:
            await update.message.reply_text(
                f"❌ Noto‘g‘ri.\nTo‘g‘ri javob: {tests[code]}"
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




