from telegram import Update
from lib.messages import getMessage
from telegram import InlineQueryResultArticle, InputTextMessageContent, InputMediaPhoto
from telegram.ext import CallbackContext
from lib.cardGenerator import (
    generateCard,
    constructOptionToCallback,
)
from lib.messages import addResume
import json, datetime, os
from lib.uploadFile import uploadFile

f = open("./assets/options.json", encoding="utf-8")
options = json.load(f)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

async def inline_caps(update: Update, context: CallbackContext):
    query = update.inline_query.query
    results = list()
    completeResume = ""
    completeResults = {}
    for option in options:
        if query == "" or query == None or option.upper().find(query.upper()) != -1:
            message, percentage = getMessage(options[option])
            completeResults[options[option]["id"]] = percentage
            if options[option]["showInResume"]:
                completeResume += message + "\n"
            results.append(
                InlineQueryResultArticle(
                    id=option.upper(),
                    title=option,
                    description=options[option]["description"],
                    input_message_content=InputTextMessageContent(message),
                    thumbnail_url=options[option]["thumbnail"],
                )
            )

    # Add summary for Ash
    results.append(addResume(completeResume))
    results.append(
        constructOptionToCallback(
            "https://static.vecteezy.com/system/resources/thumbnails/004/588/656/small/card-games-simple-black-line-web-icon-illustration-editable-stroke-48x48-pixel-perfect-free-vector.jpg",
            "https://i.ibb.co/q95R3WN/loading-min.jpg",
            800,
            1118,
            "",
        ),
    )

    await update.inline_query.answer(results, cache_time=0)

async def chosenCardOption(update: Update, context: CallbackContext):
    username = update.chosen_inline_result.from_user.first_name

    # Regenerate results
    results = {}
    for option in options:
        message, percentage = getMessage(option)
        results[options[option]["id"]] = percentage
    print("Generating card: ", datetime.datetime.now())
    fileName = generateCard(results, username, ROOT_DIR)

    # Upload to imgbb
    print("Uploading card: ", datetime.datetime.now())
    dataHost = uploadFile(
        ROOT_DIR, fileName, os.getenv("URL_UPLOAD_IMGBB"), os.getenv("APIKEY_IMGBB")
    )
    print("Editing message: ", datetime.datetime.now())
    await context.bot.edit_message_media(
        InputMediaPhoto(dataHost["data"]["medium"]["url"]),
        inline_message_id=update.chosen_inline_result.inline_message_id,
    )