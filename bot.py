from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import omdb
updater = Updater(token='550103493:AAEgg8-GP5IS2McZ_m6qny6TWQ0Iop7NJ6c') # Токен API к Telegram
dispatcher = updater.dispatcher

omdb.set_default('apikey','380310c0')

def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='''Привет,хочешь посмотреть информацию о фильме?
Какой фильм будем смотреть сегодня?:)''')
def textMessage(bot, update):
    ls=omdb.search_movie(update.message.text)
    response = 'Привет.Вот держи список.'
    #bot.send_message(chat_id=update.message.chat_id, text=response)
    print(ls)
    print(len(ls))
    if  len(ls)!=0:
        for i in ls:
            response += i['title']+'\n'
        bot.send_message(chat_id=update.message.chat_id, text=response)
        print(response)
    else:
        response = 'ничего не найдено:('
        bot.send_message(chat_id=update.message.chat_id, text=response)
        print(response)

def plotfilm(bot,update,args):
    name=' '.join(args)
    print(name)
    d=omdb.title(name,fullplot=True)
    print(d)
    newresponse=''
    if len(d)!=0:
        newresponse=d['plot']+'\nРейтинг: '+d['imdb_rating']+'\nЖанр: ' + d['genre']+'\nДлительность: '+ d['runtime']+ '\nЯзык: ' + d['language']
    else:
        newresponse='фильм не найден(:'
    bot.send_message(chat_id=update.message.chat_id, text=newresponse)


# Хендлеры
start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)
get_film_plot_command_handler = CommandHandler('plotfilm',plotfilm,pass_args='True')
# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)
dispatcher.add_handler(get_film_plot_command_handler)
# Начинаем поиск обновлений
updater.start_polling(clean=True)
# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()
