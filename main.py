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
from lib.cardGenerator.main import generateCard, constructResultPhoto
from lib.uploadFile.main import uploadFile
load_dotenv()
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) 
f = open("./assets/options.json", encoding="utf-8")
options = json.load(f)


async def start(update: Update, context):
    message = '💡 Para usar este bot, simplemente escribe "@Tucanejobot" en tu cuadro de texto y selecciona uno de los resultados (Compártelo con quien quieras).'
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

    return textToSend.format(percentage), percentage

def addResume(completeResume):
        # Add summary for Ash
    return InlineQueryResultArticle(
            id="RESUMEN",
            title="Todas las opciones a la vez",
            description="¡Obten un resumen de todos los tests a la vez!",
            input_message_content=InputTextMessageContent(
                createMessageWithTimeCheck(completeResume)
            ),
            thumb_url="https://cdn-icons-png.flaticon.com/512/86/86117.png",
        )

def createMessageWithTimeCheck(message):
     return message if not itsTheTime() else message + "\n @yenseizenit son las 22:22"

async def inline_caps(update, context):
    query = update.inline_query.query
    try:
        username = update.message.chat.username
    except:
        username = update.message.chat.first_name
    results = list()
    completeResume = ""
    completeResults = {}
    for option in options:
        if query == "" or query == None or option.upper().find(query.upper()) != -1:
            message, percentage = getMessage(option)
            completeResults[option['id']] = percentage
            if options[option]["showInResume"]:
                completeResume += message + "\n"
            results.append(
                InlineQueryResultArticle(
                    id=option.upper(),
                    title=option,
                    description=options[option]["description"],
                    input_message_content=InputTextMessageContent(message),
                    thumb_url=options[option]["thumbnail"],
                )
            )

    # Add summary for Ash
    results.append(addResume(completeResume))
    
    fileName = generateCard(completeResults,username, ROOT_DIR)
    #Upload to imgbb
    dataHost = uploadFile(ROOT_DIR, fileName, os.getenv('URL_UPLOAD_IMGBB'), os.getenv('APIKEY_IMGBB'))
    
    results.append(constructResultPhoto(dataHost['data']['thumb']['url'], dataHost['data']['url']))

    await context.bot.answer_inline_query(update.inline_query.id, results, cache_time=0)


def main():
    application = (
        ApplicationBuilder().token(os.getenv("TOKENBOT")).http_version("1.1").build()
    )
    application.add_handler(CommandHandler("start", start))
    application.add_handler(InlineQueryHandler(inline_caps))
    application.run_polling(poll_interval=1.0)


if __name__ == "__main__":
    main()