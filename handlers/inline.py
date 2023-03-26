from telegram import Update
from lib.messages import getMessage
from telegram import InlineQueryResultArticle, InputTextMessageContent, InputMediaPhoto, InlineQueryResultPhoto
from telegram.ext import CallbackContext
from lib.cardGenerator import (
    generateCard,
    constructOptionToCallback,
)
from lib.messages import addResume
import datetime, os
from lib.uploadFile import uploadFile
from definitions import ROOT_DIR, options

async def inline_caps(update: Update, context: CallbackContext):
    query = update.inline_query.query
    results = list()
    completeResume = ""
    completeResults = {}
    for option in options:
        if query == "" or query == None or option.upper().find(query.upper()) != -1:
            if not options[option]['imageGenerator']:
                message, percentage = getMessage(options[option])
                completeResults[options[option]["id"]] = percentage
                if options[option]["showInResume"]:
                    completeResume += message + "\n"
                results.append(
                    InlineQueryResultArticle(
                        id=options[option]['id'],
                        title=option,
                        description=options[option]["description"],
                        input_message_content=InputTextMessageContent(message),
                        thumbnail_url=options[option]["thumbnail"],
                    )
                )
            else:
                results.append(
                    InlineQueryResultPhoto(
                        id=options[option]['id'],
                        title=option,
                        description=options[option]["description"],
                        photo_url=options[option]["thumbnail"],
                        thumbnail_url=options[option]["thumbnail"],
                        photo_height=options[option]['height'],
                        photo_width=options[option]['width'],
                        reply_markup=options[option]['reply_markup'],
                    )
                )

    # Add summary option
    results.append(addResume(completeResume))

    await update.inline_query.answer(results, cache_time=0)

async def chosenCardOption(update: Update, context: CallbackContext):
    username = update.chosen_inline_result.from_user.first_name

    # Regenerate results
    results = {}
    for option in options:
        if not options[option]['imageGenerator']:
            message, percentage = getMessage(options[option])
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