from telegram.ext import Application, CommandHandler
from config import TOKEN
from handlers import start, study, create_test_conv

async def main():
    application = Application.builder().token(TOKEN).build()
    
    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("study", study))
    application.add_handler(create_test_conv)
    
    await application.run_polling()
