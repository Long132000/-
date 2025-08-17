import logging
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
import pytz



# Заменим casino.db на более подходящее имя
DATABASE_FILE = 'python_learning_bot.db'

# Состояния для ConversationHandler
CHOOSE_TOPIC, CREATE_QUESTION, CREATE_ANSWER, TEST_MODE = range(4)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)  # Исправлено на __name__ для корректных логов

# Функция старта
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Добро пожаловать! Начните создание теста, отправив команду /createtest.")

# Обработчик для создания теста
async def create_test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Введите тему теста:")
    return CHOOSE_TOPIC

# Обработчик для ввода вопроса
async def create_question_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['question'] = update.message.text
    await update.message.reply_text("Введите ответ на вопрос:")
    return CREATE_ANSWER

# Обработчик для ввода ответа
async def create_answer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    answer = update.message.text
    question = context.user_data['question']
    # Здесь можно добавить код для записи вопроса и ответа в базу данных
    await update.message.reply_text("Тест создан! Вы можете пройти тест сейчас.")
    return TEST_MODE

# Обработчик для прохождения теста
async def test_mode_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Вы находитесь в режиме теста.")
    return ConversationHandler.END

# Функция для обработки ошибок
def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.warning(f'Update "{update}" caused error "{context.error}"')

def main():
    application = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("createtest", create_test)],
        states={
            CHOOSE_TOPIC: [MessageHandler(filters.text & ~filters.command, create_question_handler)],
            CREATE_QUESTION: [MessageHandler(filters.text & ~filters.command, create_question_handler)],
            CREATE_ANSWER: [MessageHandler(filters.text & ~filters.command, create_answer_handler)],
            TEST_MODE: [MessageHandler(filters.text & ~filters.command, test_mode_handler)],
        },
        fallbacks=[CommandHandler("cancel", start)],
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)
    application.add_error_handler(error)
    application.run_polling()
    application = ApplicationBuilder().token("YOUR_BOT_TOKEN").time_zone(pytz.timezone("Europe/Moscow")).build()

if __name__ == '__main__':  # Исправлено на __name__ для корректного запуска
    main()
