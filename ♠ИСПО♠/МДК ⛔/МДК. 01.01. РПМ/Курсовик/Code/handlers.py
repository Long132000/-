from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)
from database import Session, Test, Question, Answer, UserProgress

# Стадии разговора для создания теста
CREATE_TEST, ADD_QUESTION, ADD_ANSWERS, ADD_CORRECT_ANSWER = range(4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я помогу тебе изучить Python.\n"
        "Доступные команды:\n"
        "/study - Учебные материалы\n"
        "/tests - Пройти тесты\n"
        "/create_test - Создать тест (для администраторов)"
    )

async def study(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Здесь можно добавить логику вывода учебных материалов
    await update.message.reply_text("Разделы обучения:\n1. Основы синтаксиса\n2. Структуры данных...")

async def start_create_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("Эта команда доступна только администраторам")
        return ConversationHandler.END
    await update.message.reply_text("Введите название теста:")
    return CREATE_TEST

async def create_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = Session()
    new_test = Test(title=update.message.text)
    session.add(new_test)
    session.commit()
    context.user_data['current_test'] = new_test.id
    await update.message.reply_text("Тест создан! Теперь введите первый вопрос:")
    return ADD_QUESTION

async def add_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = Session()
    new_question = Question(
        text=update.message.text,
        test_id=context.user_data['current_test']
    )
    session.add(new_question)
    session.commit()
    context.user_data['current_question'] = new_question.id
    await update.message.reply_text("Введите варианты ответов через точку с запятой (;):")
    return ADD_ANSWERS

async def add_answers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answers = update.message.text.split(';')
    context.user_data['answers'] = answers
    await update.message.reply_text("Укажите номер правильного ответа:")
    return ADD_CORRECT_ANSWER

async def add_correct_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = Session()
    try:
        correct_index = int(update.message.text) - 1
        answers = context.user_data['answers']
        
        question = session.query(Question).get(context.user_data['current_question'])
        
        for i, answer_text in enumerate(answers):
            is_correct = (i == correct_index)
            answer = Answer(text=answer_text.strip(), is_correct=is_correct, question=question)
            session.add(answer)
        
        session.commit()
        await update.message.reply_text("Ответы добавлены! Введите следующий вопрос или /cancel для завершения")
        return ADD_QUESTION
    except:
        await update.message.reply_text("Ошибка! Попробуйте снова")
        return ADD_CORRECT_ANSWER

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Создание теста отменено")
    return ConversationHandler.END
#------------------
# async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_id = update.effective_user.id
#     await update.message.reply_text(f"Ваш ID: {user_id}")
#------------------

# Собираем ConversationHandler для создания теста
create_test_conv = ConversationHandler(
    entry_points=[CommandHandler('create_test', start_create_test)],
    states={
        CREATE_TEST: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_test)],
        ADD_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_question)],
        ADD_ANSWERS: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_answers)],
        ADD_CORRECT_ANSWER: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_correct_answer)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

