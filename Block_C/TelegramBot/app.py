import telebot
from config import TOKEN
from extensions import CryptoConverter, ConvertionException

bot = telebot.TeleBot(TOKEN)
keys = CryptoConverter.get_values()

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следющем формате:\n<имя валюты>  \
<в какую валюту переводим><количество переводимой валюты>\nУвидеть список всех \
доступных валют: /values\nДобавить еще валюту для конвертации /addvalues <название валюты> <тикер валюты (например USD)>'
    bot.reply_to(message, text)


@bot.message_handler(commands=['addvalue'])
def handler_addvalue(message: telebot.types.Message):
    try:
        value = message.text.split(' ')
        if len(value) != 3:
            raise ConvertionException('Неверное количество параметров')
        name = value[1].lower()
        ticker = value[2].upper()
        CryptoConverter.add_values(name, ticker, keys)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        bot.send_message(message.chat.id, f'Валюта {name} успешко добавлена')


@bot.message_handler(commands=['values'])
def handle_values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['audio', 'photo', 'voice', 'video', 'document', 'location', 'contact', 'sticker'])
def handle_other_content(message: telebot.types.Message):
    bot.reply_to(message, "Я не умею обрабатывать данный контент")


@bot.message_handler(content_types=['text'])
def handle_convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')
        if len(values) != 3:
            raise ConvertionException('Неверное количество параметров')
        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount, keys)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()