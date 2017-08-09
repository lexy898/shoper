import telebot
import logging
from telebot import types

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')

token = "426617203:AAHqKOH-62wRF1XSEFR8NS6372nHMWNR0BE"

bot = telebot.TeleBot(token)

def sendMessage(new_things):
    text_message = "Появились новые товары со скидкой в магазине H&M!\n"
    for i in range(len(new_things)):
        text_message += new_things[i][3]+" "+str(new_things[i][2])+"Руб (Старая цена "\
                        +str(new_things[i][1])+"Руб.)\n"
        text_message += "Скидка: "+str(discountCount(new_things[i][2],new_things[i][1]))+"%\n"
        text_message += "Размеры: "+formatSize(new_things[i][4])+"\n"
        text_message +="http://www2.hm.com/ru_ru/productpage." + new_things[i][0] + ".html\n\n"
    try:
        bot.send_message(158041048, text_message)
    except ValueError as err:
        logging.error(u'Ошибка Telegram при отправке сообщения' + str(err))

def formatSize(size):
    result = ""
    for i in range(len(size)):
        result+= size[i].split('_', 1)[1]+"; "
    return result

def discountCount(newPrice, oldPrice):
    discount = round(100-(newPrice/oldPrice)*100)
    return discount

'''''
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    markup = types.ReplyKeyboardMarkup()
    markup.row('Мои подписки','Бренды')
    markup.row('🚫')
    bot.send_message(message.chat.id, "Choose one letter:", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "Мои подписки":
        bot.send_message(message.chat.id, "Твои подписки")
    elif message.text == "Бренды":
        bot.send_message(message.chat.id, "Список брендов")
    elif message.text == "🚫":
        markdown = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, "Пока 😜", reply_markup=markdown)
    else:
        bot.send_message(message.chat.id, "Не понимаю, что ты мне хочешь сказать")

@bot.message_handler(commands=['chatID'])
def handle_start_help(message):
    bot.send_message(message.chat.id, message.chat.id)

bot.polling(none_stop=True, interval=0)
'''''