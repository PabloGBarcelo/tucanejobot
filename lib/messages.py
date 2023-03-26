import time, random
from telegram import InlineQueryResultArticle, InputTextMessageContent


def getMessage(option):
    random.seed(time.perf_counter())
    percentage = random.randint(option["min"], option["max"])
    if percentage == option["min"]:
        textToSend = option["result"]["min"]
    elif percentage == option["max"]:
        textToSend = option["result"]["max"]
    else:
        textToSend = option["result"]["default"]

    return textToSend.format(percentage), percentage


def addResume(completeResume):
    # Add summary for Ash
    return InlineQueryResultArticle(
        id="RESUMEN",
        title="Todas las opciones a la vez",
        description="¡Obten un resumen de todos los tests a la vez!",
        input_message_content=InputTextMessageContent(completeResume),
        thumbnail_url="https://cdn-icons-png.flaticon.com/512/86/86117.png",
    )
