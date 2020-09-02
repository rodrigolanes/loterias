import logging
import os

from dotenv import load_dotenv
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from utils.format import formata_concurso_text
from utils.sqlite_helper import add_usuario, get_last_concurso

load_dotenv()

telegram_token = os.getenv("TELEGRAM_TOKEN")

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    mensagem = """Oi, Sou o bot da Boa Sorte!

Eu envio mensagem sobre os jogos da Mega Sena sempre que um novo resultado é publicado no site da Caixa Econômica Federal.

Aguarde pelo próximo concurso e enviarei o resultado."""
    add_usuario(update.message.from_user.id)
    update.message.reply_text(mensagem)


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def ultimo_concurso(update, context):
    """Responde o último consurso da mega_sena."""
    update.message.reply_text(
        formata_concurso_text(get_last_concurso()), parse_mode="MARKDOWN")


def main():
    """Start the bot."""
    updater = Updater(
        telegram_token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
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
