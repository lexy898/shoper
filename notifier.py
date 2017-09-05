import telebot
import logging
import config
from telebot import util
import sqlRequests

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')

TOKEN = config.getToken()
bot = telebot.TeleBot(TOKEN)
brands = sqlRequests.getBrandsInvert()

def sendMessageHnM(new_things, type, company):
    text_message = "Появились новые товары со скидкой в магазине "+company+"!\n"
    id = sqlRequests.getIdTypesOfGoodByType(type)
    text_message += str(sqlRequests.getDescriptionByTypeOfGood(type))+": \n\n"
    subscribers = sqlRequests.getSubscribers(brands[company],sqlRequests.getIdTypesOfGoodByType(type))

    for thing in new_things:
        text_message += "⭐️"+thing[3]+"\n"
        text_message += "Цена: "+str(thing[2])+"Руб\n"
        text_message += "Старая цена: " + str(thing[1]) + "Руб\n"
        text_message += "Скидка: "+str(discountCount(thing[2],thing[1]))+"%\n"
        if thing[4] != '-':
            text_message += "Размеры: "+formatSize(thing[4])+"\n"
        text_message +=config.getProductPage(company) + thing[0] + ".html\n\n"
    try:
        splitted_text = util.split_string(text_message, 3000)
        for text in splitted_text:
            for subscriber in subscribers:
                bot.send_message(subscriber, text)
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
    discount = 0
    try:
        discount = round(100-(float(newPrice)/float(oldPrice))*100)
    except ZeroDivisionError as err:
        logging.error(u'Ошибка Деления на 0' + str(err))
    finally:
        return discount
