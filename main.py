import json
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

DATA_FILE = "data.json"
TURKCULUK_GIF = "https://media.giphy.com/media/h2JYcqBkskT2A/giphy.gif"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"users": [], "groups": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    chat = update.effective_chat

    if chat.type == "private":
        if chat.id not in data["users"]:
            data["users"].append(chat.id)
            save_data(data)

        await context.bot.send_animation(chat_id=chat.id, animation=TURKCULUK_GIF)

        keyboard = [
            [InlineKeyboardButton("🧾 Komutlar", callback_data="komutlar")],
            [InlineKeyboardButton("❓ Yardım", callback_data="yardim")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_message(
            chat_id=chat.id,
            text="🇹🇷 *Kızıl Sancak'a Hoş Geldin!*",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    elif chat.type in ["group", "supergroup"]:
        if chat.id not in data["groups"]:
            data["groups"].append(chat.id)
            save_data(data)
        await update.message.reply_text("🟥 Kızıl Sancak bu gruba başarıyla bağlandı.")

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "komutlar":
        msg = "📜 Komutlar:\n/start - Başlat\n/help - Yardım\n/istatistik - Kullanıcı ve Grup Sayısı"
        await query.edit_message_text(msg)
    elif query.data == "yardim":
        msg = "🔴 12 Ülkenin birleştiği Tek Blok: *Kızıl Sancak Üretimiyim.*"
        await query.edit_message_text(msg, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "🔴 12 Ülkenin birleştiği Tek Blok: *Kızıl Sancak Üretimiyim.*"
    await update.message.reply_text(msg, parse_mode="Markdown")

async def istatistik(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    users = len(data["users"])
    groups = len(data["groups"])
    msg = f"📊 *Kızıl Sancak İstatistikleri*\n👤 Kullanıcı Sayısı: {users}\n👥 Grup Sayısı: {groups}"
    await update.message.reply_text(msg, parse_mode="Markdown")

async def main():
    import os
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        print("🚫 BOT_TOKEN çevresel değişkeni tanımlanmadı!")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("istatistik", istatistik))
    app.add_handler(CallbackQueryHandler(handle_button))

    print("🔴 Kızıl Sancak Botu Aktif")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
