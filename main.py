# -*- coding: utf-8 -*-
import random, os
from dotenv import load_dotenv
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    InlineQueryHandler,
)
import time
import json

load_dotenv()
f = open("./assets/options.json", encoding="utf-8")
options = json.load(f)


async def start(update: Update, context):
    message = "💡 Para usar este bot, simplemente escribe \"@Tucanejobot\" en tu cuadro de texto y selecciona uno de los resultados (Compártelo con quien quieras)."
    await update.message.reply_text(message)


def getMessage(type):
    random.seed(time.perf_counter())
    percentage = random.randint(options[type]["min"], options[type]["max"])
    if percentage == options[type]["min"]:
        textToSend = options[type]["result"]["min"]
    elif percentage == options[type]["max"]:
        textToSend = options[type]["result"]["max"]
    else:
        textToSend = options[type]["result"]["default"]

    return textToSend.format(percentage)


async def unknown(update, context):
    await update.message.reply_text("Lo siento, no entiendo esa opción.")


async def inline_caps(update, context):
    query = update.inline_query.query
    results = list()
    for option in options:
        if query == "" or query == None or option.upper().find(query.upper()) != -1:
            results.append(
                InlineQueryResultArticle(
                    id=option.upper(),
                    title=option.upper(),
                    description=options[option]["description"],
                    input_message_content=InputTextMessageContent(
                        getMessage(option.upper())
                    ),
                    thumb_url=options[option]["thumbnail"],
                )
            )
    await context.bot.answer_inline_query(update.inline_query.id, results, cache_time=0)


def main():
    application = (
        ApplicationBuilder().token(os.getenv("TOKENBOT")).http_version("1.1").build()
    )
    application.add_handler(CommandHandler('start', start))
    application.add_handler(InlineQueryHandler(inline_caps))
    application.run_polling(poll_interval=1.0)


if __name__ == "__main__":
    main()
