# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    InlineQueryHandler,
    ChosenInlineResultHandler,
)

from handlers.start import start
from handlers.inline import inline_caps, chosenCardOption

load_dotenv()

def main():
    application = (
        ApplicationBuilder().token(os.getenv("TOKENBOT")).http_version("1.1").build()
    )
    application.add_handler(CommandHandler("start", start))
    application.add_handler(InlineQueryHandler(inline_caps))
    application.add_handler(
        ChosenInlineResultHandler(chosenCardOption, pattern="Medalla")
    )
    application.run_polling(poll_interval=1.0)


if __name__ == "__main__":
    main()
