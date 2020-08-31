import logging
import os

from dotenv import load_dotenv
from telegram.ext import (CommandHandler, Filters, MessageHandler,
                          PicklePersistence, Updater)

load_dotenv()

my_persistence = PicklePersistence(filename='data.bak')

telegram_token = os.getenv("TELEGRAM_TOKEN")

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""

    if not "users_id" in context.bot_data:
        context.bot_data["users_id"] = set()

    context.bot_data["users_id"].add(update.message.from_user.id)

    mensagem = """Oi, Sou o bot da Boa Sorte!

Eu envio mensagem sobre os jogos da Mega Sena sempre que um novo resultado é publicado no site da Caixa Econômica Federal.

Aguarde pelo próximo concurso e enviarei o resultado."""
    update.message.reply_text(mensagem)


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def ultimo_concurso(update, context):
    """Responde o último consurso da mega_sena."""
    update.message.reply_text('Último!')


def main():
    """Start the bot."""
    updater = Updater(
        telegram_token, persistence=my_persistence, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    # dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("ultimo", ultimo_concurso))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
