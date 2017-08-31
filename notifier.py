import telebot
import logging
from telebot import util
import sqlRequests

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')

token = "426617203:AAHqKOH-62wRF1XSEFR8NS6372nHMWNR0BE"
bot = telebot.TeleBot(token)
brands = sqlRequests.getBrandsInvert()

def sendMessageHnM(new_things, type, company):
    text_message = "Появились новые товары со скидкой в магазине "+company+"!\n"
    if type == 'male':
        text_message += "💪🏼Мужское: \n\n"
        subscribers = sqlRequests.getSubscribers(brands[company],1)
    elif type == 'female':
        text_message += "👠Женское: \n\n"
        subscribers = sqlRequests.getSubscribers(brands[company], 2)
    elif type == 'childrens':
        text_message += "🎒Детское: \n\n"
        subscribers = sqlRequests.getSubscribers(brands[company], 3)
    elif type == 'HOME':
        text_message += "🍷H&M HOME: \n\n"
        subscribers = sqlRequests.getSubscribers(brands[company], 4)
    else:
        return 0
    for thing in new_things:
        text_message += "⭐️"+thing[3]+" "+str(thing[2])+"Руб (Старая цена "\
                        +str(thing[1])+"Руб.)\n"
        text_message += "Скидка: "+str(discountCount(thing[2],thing[1]))+"%\n"
        if thing[4] != '-':
            text_message += "Размеры: "+formatSize(thing[4])+"\n"
        text_message +="http://www2.hm.com/ru_ru/productpage." + thing[0] + ".html\n\n"
    try:
        splitted_text = util.split_string(text_message, 3000)
        for text in splitted_text:
            for i in range(len(subscribers)):
                bot.send_message(subscribers[i], text)
    except ValueError as err:
        logging.error(u'Ошибка Telegram при отправке сообщения' + str(err))

def formatSize(size):
    result = ""
    try:
        for i in range(len(size)):
            result+= size[i].split('_', 1)[1]+"; "
    except:
        result = size
    return result

def discountCount(newPrice, oldPrice):
    discount = round(100-(float(newPrice)/float(oldPrice))*100)
    return discount
