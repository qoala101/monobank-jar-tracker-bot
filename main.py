import logging
import monobank
from telegram import Update
from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def RemoveJobIfExists(name: str, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.job_queue is None:
        return

    current_jobs = context.job_queue.get_jobs_by_name(name)

    if current_jobs is None:
        return

    for job in current_jobs:
        job.schedule_removal()


async def OnTick(context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.job is None or context.job.chat_id is None:
        return

    await context.bot.send_message(
        context.job.chat_id, text=f"Jar is: {context.job.data}"
    )


async def OnJar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message

    if (
        message is None
        or message.text is None
        or context is None
        or context.args is None
        or context.job_queue is None
    ):
        return

    try:
        jar_uri = context.args[0]
        price = float(context.args[1])
        people = int(context.args[2])
    except:
        await message.reply_text("Usage: /jar <URL> <price> <people>")
        return

    chat_id = str(message.chat_id)
    RemoveJobIfExists(chat_id, context)

    context.job_queue.run_repeating(
        callback=OnTick,
        interval=10,
        chat_id=message.chat_id,
        data=jar_uri,
        name=chat_id,
    )

    await message.reply_text("Timer is set")


async def OnUnknownCommand(update: Update, _) -> None:
    if update.effective_message is None:
        return

    await update.effective_message.reply_text(
        "Unknown command. Supported commands: /jar JAR_URI PRICE NUM_PEOPLE"
    )


def main() -> None:
    token_file = open("token.txt", "r")
    token = token_file.read()

    application = ApplicationBuilder().token(token).build()
    application.add_handler(CommandHandler("jar", OnJar))
    application.add_handler(MessageHandler(filters.COMMAND, OnUnknownCommand))
    application.run_polling()


if __name__ == "__main__":
    main()
