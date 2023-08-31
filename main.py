import logging
import monobank
from telegram import Update
from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    CommandHandler,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def OnJar(update: Update, _):
    if (
        update.message is None
        or update.message.text is None
        or update.effective_chat is None
    ):
        return

    _, jar_uri, price, num_people = update.message.text.split()

    short_jar_id = monobank.GetShortIdFromJarUri(jar_uri)
    long_jar_id = monobank.FetchLongJarId(short_jar_id)
    jar_amount = monobank.FetchJarAmount(long_jar_id)

    await update.message.reply_text(str(jar_amount))


async def OnUnknownCommand(update: Update, _):
    if update.message is None:
        return

    await update.message.reply_text(
        "Unknown command. Supported commands: /jar JAR_URI PRICE NUM_PEOPLE"
    )


def main():
    token_file = open("token.txt", "r")
    token = token_file.read()

    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler("jar", OnJar))
    application.add_handler(MessageHandler(filters.COMMAND, OnUnknownCommand))
    application.run_polling()


if __name__ == "__main__":
    main()
