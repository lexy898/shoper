import telebot
import logging
import config
from telebot import util
import sql_requests

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')

TOKEN = config.get_token()
bot = telebot.TeleBot(TOKEN)
brands = sql_requests.get_brands_invert()

def send_message(new_things, type, company):
    text_message = "Появились новые товары со скидкой в магазине "+company+"!\n"
    id = sql_requests.get_id_types_of_good_by_type(type)
    text_message += str(sql_requests.get_description_by_type_of_good(type)) + ": \n\n"
    subscribers = sql_requests.get_subscribers(brands[company], sql_requests.get_id_types_of_good_by_type(type))
    for thing in new_things:
        text_message += "⭐️"+thing[3]+"\n"
        text_message += "Цена: "+str(thing[2])+"Руб\n"
        text_message += "Старая цена: " + str(thing[1]) + "Руб\n"
        text_message += "Скидка: "+str(discount_count(thing[2], thing[1])) + "%\n"
        if thing[4] != '-':
            text_message += "Размеры: " + format_size(thing[4]) + "\n"
        text_message += thing[5]+"\n\n"
    try:
        splitted_text = util.split_string(text_message, 3000)
        for text in splitted_text:
            for subscriber in subscribers:
                bot.send_message(subscriber, text)
    except ValueError as err:
        logging.error(u'Ошибка Telegram при отправке сообщения' + str(err))

def format_size(sizes):
    result = ''
    for size in sizes:
        try:
            result += size.split('_', 1)[1]+"; "
        except:
            result += str(size)+"; "
    return result

def discount_count(newPrice, oldPrice):
    discount = 0
    try:
        discount = round(100-(float(newPrice)/float(oldPrice))*100)
    except ZeroDivisionError as err:
        logging.error(u'Ошибка Деления на 0' + str(err))
    finally:
        return discount
