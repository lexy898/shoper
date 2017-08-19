import telebot
import logging
from telebot import util

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')

token = "426617203:AAHqKOH-62wRF1XSEFR8NS6372nHMWNR0BE"
chat_id = 158041048

bot = telebot.TeleBot(token)

def sendMessage(new_things):
    text_message = "Появились новые товары со скидкой в магазине H&M!\n"
    for i in range(len(new_things)):
        text_message += "⭐️"+new_things[i][3]+" "+str(new_things[i][2])+"Руб (Старая цена "\
                        +str(new_things[i][1])+"Руб.)\n"
        text_message += "Скидка: "+str(discountCount(new_things[i][2],new_things[i][1]))+"%\n"
        text_message += "Размеры: "+formatSize(new_things[i][4])+"\n"
        text_message +="http://www2.hm.com/ru_ru/productpage." + new_things[i][0] + ".html\n\n"
    try:
        splitted_text = util.split_string(text_message, 3000)
        for text in splitted_text:
            bot.send_message(chat_id, text)
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