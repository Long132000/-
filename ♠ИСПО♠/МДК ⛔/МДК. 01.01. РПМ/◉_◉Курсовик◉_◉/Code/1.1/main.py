from telegram.ext import Updater
from config import TOKEN
from handlers import start, study, create_test_conv

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Регистрация обработчиков
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("study", study))
    dispatcher.add_handler(create_test_conv)

    updater.start_polling()
    updater.idle()
#------------------
    # application.add_handler(CommandHandler("get_id", get_id))
#------------------
if __name__ == "__main__":
    main()


# from telegram.ext import Application, CommandHandler
# from config import TOKEN
# from handlers import start, study, create_test_conv
# import asyncio

# async def main():
#     application = Application.builder().token(TOKEN).build()
    
#     # Регистрация обработчиков
#     application.add_handler(CommandHandler("start", start))
#     application.add_handler(CommandHandler("study", study))
#     application.add_handler(create_test_conv)
    
#     await application.run_polling()

# if __name__ == "__main__":
#     asyncio.run(main())
