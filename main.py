import os, threading, logging
import stripe
from flask import Flask, request, abort
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler
from dotenv import load_dotenv

load_dotenv()

TOKEN      = os.getenv("TG_TOKEN")
PRICE_ID   = os.getenv("STRIPE_PRICE_ID")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
GROUP_IDS  = [-1001800495596, -1002280101284, -1002516382967]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
bot = Bot(TOKEN)

def start(update: Update, context):
    kb = [[InlineKeyboardButton("🔓 UNISCITI ORA", url=f"https://buy.stripe.com/{PRICE_ID}")]]
    text = (
        "🎯 Benvenuto nel bot ufficiale scalper.sam!\n\n"
        "🔐 Clicca per sbloccare l’accesso privato (49,88€)."
    )
    update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))

def run_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    logger.info("Bot avviato in polling…")
    updater.idle()

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "OK", 200

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
