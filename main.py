from flask import Flask, request, redirect
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ContextTypes
)
import urllib.parse
import threading

# --- Flask App ---
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ PW Redirect API is Live"

@app.route('/live')
def redirector():
    raw_url = request.args.get("q")
    if not raw_url:
        return "❌ Missing 'q' parameter", 400
    return redirect(raw_url, code=302)

# --- Telegram Bot Logic ---

BOT_TOKEN = "8067349631:AAEypPktMhYoL3aMH90u0d33R_U8tbU7WTg"  # 👈 Your Token

# Replace with Railway app base URL
RAILWAY_BASE = "https://<your-railway-url>.railway.app/live"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me any PW video link (.mp4), I’ll give you 1DM download link.")

async def handle_pw_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    raw_link = update.message.text.strip()
    if not raw_link.startswith("http"):
        await update.message.reply_text("❌ Invalid link. Please send a proper PW video link.")
        return

    try:
        encoded = urllib.parse.quote(raw_link, safe='')
        final = f"{RAILWAY_BASE}?q={encoded}&n=PW-Lecture"
        await update.message.reply_text(f"✅ 1DM Link:\n{final}")
    except Exception as e:
        await update.message.reply_text("❌ Failed to convert.")
        print("Error:", e)

def start_telegram():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_pw_link))
    app.run_polling()

# --- Run Flask + Telegram in same app ---
if __name__ == "__main__":
    threading.Thread(target=start_telegram).start()
    app.run(host="0.0.0.0", port=8080)
