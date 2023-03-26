from telegram import Update

async def start(update: Update, context):
    message = '💡 Para usar este bot, simplemente escribe "@Tucanejobot" en tu cuadro de texto y selecciona uno de los resultados (Compártelo con quien quieras).'
    await update.message.reply_text(message)
