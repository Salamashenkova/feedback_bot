from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

# Определим этапы разговора
NAME, FEEDBACK = range(2)

# Функция старта
def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Привет! Введите свое ФИО?")
    return NAME

# Функция для обработки имени
def get_name(update: Update, context: CallbackContext) -> int:
    user_name = update.message.text
    context.user_data['name'] = user_name  # Сохраняем имя в user_data
    update.message.reply_text(f"Спасибо, {user_name}! Теперь, пожалуйста, оставь свой фидбэк.")
    return FEEDBACK

# Функция для обработки фидбэка
def get_feedback(update: Update, context: CallbackContext) -> int:
    feedback = update.message.text
    user_name = context.user_data['name']
    # Отправляем фидбэк вам
    context.bot.send_message(chat_id='960932250', text=f"Фидбэк от {user_name}: {feedback}")
    # Сохраняем имя и фидбэк в файл
    #with open('feedback.txt', 'a') as f:
        #f.write(f"Имя: {user_name}, Фидбэк: {feedback}\n")
    update.message.reply_text("Спасибо за ваш фидбэк! Если хотите, напишите /start для нового ввода.")
    return ConversationHandler.END

# Функция для завершения разговора
def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Диалог закончен. Если захотите отсавить еще отзыв, просто напишите /start.")
    return ConversationHandler.END

# Основная функция для запуска бота
def main() -> None:
    updater = Updater("7624032594:AAEHtduiBwzbG_pDpaKu8REXRcvb0f0aQRQ")

    # Обработчик разговоров
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, get_name)],
            FEEDBACK: [MessageHandler(Filters.text & ~Filters.command, get_feedback)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    updater.dispatcher.add_handler(conv_handler)

    # Запускаем бот
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
