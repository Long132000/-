import telegram
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
import os

# Состояния для разговора о создании теста
(TOP_LEVEL, TEST_NAME, QUESTION, ANSWER, ADD_MORE, RUN_TEST, CHECK_ANSWER) = range(7)

DATABASE_FILE = "db.txt"

def load_data():
    data = {}
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r", encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if "=" in line:
                    key, value = line.split("=", 1)
                    data[key] = value.replace('\\n', '\n')
                else:
                    print(f"Пропускаю некорректную строку: {line}")
    return data

def save_data(data):
    with open(DATABASE_FILE, "w", encoding='utf-8') as f:
        for key, value in data.items():
            escaped_value = value.replace('\n', '\\n')
            f.write(f"{key}={escaped_value}\n")

async def start(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Привет, {user.first_name}! Я бот для изучения Python с конструктором тестов.\nИспользуйте /help для списка команд.")

async def help_command(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
    Доступные команды:
    /start - Начать работу с ботом
    /help - Показать это сообщение
    /create_test - Создать новый тест
    /resources - Полезные ресурсы
    /list_tests - Список тестов
    /run_test - Запустить тест
    """
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

async def resources(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    resource_text = """
    Полезные ресурсы:
    - Официальная документация Python: https://docs.python.org/3/
    - Learn Python: https://www.learnpython.org/
    """
    await context.bot.send_message(chat_id=update.effective_chat.id, text=resource_text)

async def list_tests(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    if not data:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Нет доступных тестов.")
    else:
        test_list = "\n".join(data.keys())
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Список тестов:\n{test_list}")

async def create_test(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Давайте создадим новый тест! Как назовем тест?")
    return TEST_NAME

async def test_name(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['test_name'] = update.message.text
    context.user_data['questions'] = []
    await update.message.reply_text(f"Название теста: {context.user_data['test_name']}.\nВведите первый вопрос:")
    return QUESTION

async def question(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['current_question'] = update.message.text
    await update.message.reply_text("Введите ответ на этот вопрос:")
    return ANSWER

async def answer(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    qa = {
        'question': context.user_data['current_question'],
        'answer': update.message.text
    }
    context.user_data['questions'].append(qa)
    await update.message.reply_text("Вопрос добавлен. Добавить еще? (да/нет)")
    return ADD_MORE

async def add_more(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text.lower() == 'да':
        await update.message.reply_text("Введите следующий вопрос:")
        return QUESTION
    else:
        test_name = context.user_data['test_name']
        data = load_data()
        test_data = "\n".join([f"{q['question']}||{q['answer']}" for q in context.user_data['questions']])
        data[test_name] = test_data
        save_data(data)
        await update.message.reply_text(f"Тест '{test_name}' сохранен!")
        return ConversationHandler.END

async def cancel(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Отменено.")
    return ConversationHandler.END

async def run_test(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    data = load_data()
    if not data:
        await update.message.reply_text("Нет тестов.")
        return ConversationHandler.END
    # Исправленная часть:
    test_list = "\n".join(data.keys())
    await update.message.reply_text(f"Выберите тест:\n{test_list}")
    return RUN_TEST

async def choose_test(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    test_name = update.message.text
    data = load_data()
    if test_name not in data:
        await update.message.reply_text("Тест не найден.")
        return RUN_TEST
    test_data = data[test_name].split("\n")
    questions = []
    for line in test_data:
        if '||' in line:
            q, a = line.split("||", 1)
            questions.append({'question': q, 'answer': a})
    context.user_data['questions'] = questions
    context.user_data['current_index'] = 0
    context.user_data['correct'] = 0
    await ask_question(update, context)
    return CHECK_ANSWER

async def ask_question(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    index = context.user_data['current_index']
    question = context.user_data['questions'][index]['question']
    await update.message.reply_text(f"Вопрос {index + 1}:\n{question}")

async def check_answer(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_answer = update.message.text
    index = context.user_data['current_index']
    correct_answer = context.user_data['questions'][index]['answer']
    
    if user_answer.strip().lower() == correct_answer.strip().lower():
        context.user_data['correct'] += 1
        await update.message.reply_text("✅ Правильно!")
    else:
        await update.message.reply_text(f"❌ Неправильно. Правильный ответ: {correct_answer}")
    
    context.user_data['current_index'] += 1
    if context.user_data['current_index'] < len(context.user_data['questions']):
        await ask_question(update, context)
        return CHECK_ANSWER
    else:
        total = len(context.user_data['questions'])
        correct = context.user_data['correct']
        await update.message.reply_text(f"Тест завершен! Правильных ответов: {correct} из {total}")
        return ConversationHandler.END

async def error_handler(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Ошибка: {context.error}")

def main():
    BOT_TOKEN = "8163976255:AAE3q2xvrN3fmzjrODK4QlfsuQoPzTF5QOQ"
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("resources", resources))
    app.add_handler(CommandHandler("list_tests", list_tests))

    conv_create = ConversationHandler(
        entry_points=[CommandHandler('create_test', create_test)],
        states={
            TEST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, test_name)],
            QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, question)],
            ANSWER: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer)],
            ADD_MORE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_more)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    app.add_handler(conv_create)

    conv_run = ConversationHandler(
        entry_points=[CommandHandler('run_test', run_test)],
        states={
            RUN_TEST: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_test)],
            CHECK_ANSWER: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_answer)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    app.add_handler(conv_run)

    app.add_error_handler(error_handler)
    
    if not os.path.exists(DATABASE_FILE):
        save_data({
            "print_test": "Что делает print()?||Выводит текст",
            "input_test": "Как получить ввод?||input()",
            "if_test": "Как проверить условие?||if"
        })

    app.run_polling()

if __name__ == '__main__':
    main()