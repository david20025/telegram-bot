from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import omdb

updater = Updater(token='Ваш Api')  # Токен API к Telegram
dispatcher = updater.dispatcher

omdb.set_default('apikey', 'Ваш ключ')


def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='''Привет,
    хочешь посмотреть информацию о фильме?
Какой фильм будем смотреть сегодня?:)''')


def textMessage(bot, update):
    ls = omdb.search_movie(update.message.text)
    response = 'Привет.Вот держи список.\n'
    if len(ls) != 0:
        for i in ls:
            response += i['title'] + '\n'
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        response = 'ничего не найдено:('
        bot.send_message(chat_id=update.message.chat_id, text=response)


def plotfilm(bot, update, args):
    name = ' '.join(args)
    d = omdb.title(name, fullplot=True)
    newresponse = ''
    if len(d) != 0:
        newresponse = d['plot'] + '\nРейтинг: ' + d['imdb_rating'] + '\nЖанр: '
        newresponse += d['genre'] + '\nДлительность: '
        newresponse += d['runtime'] + '\nЯзык: '
        newresponse += d['language']
    else:
        newresponse = 'фильм не найден:('
    bot.send_message(chat_id=update.message.chat_id, text=newresponse)


# Хендлеры
start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)
get_film_plot = CommandHandler('plotfilm', plotfilm, pass_args='True')
# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)
dispatcher.add_handler(get_film_plot)
# Начинаем поиск обновлений
updater.start_polling(clean=True)
# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()
