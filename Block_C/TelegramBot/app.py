import telebot

bot = telebot.TeleBot("6364681085:AAHaMDlhfdXmiAeErbLTI6CmbKtauBPH1nQ")


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, f"bla bla bla {message.chat.username}")


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.reply_to(message, "зачетное фото")


@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    pass

bot.polling(none_stop=True)