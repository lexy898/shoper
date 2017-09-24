import telebot
from telebot import util
import sql_requests
import config

TOKEN = config.get_token()
bot = telebot.TeleBot(TOKEN)
allSubscribers = sql_requests.get_all_subscribers()
print(allSubscribers)
TEXT = '🌈Появился новый магазин Adidas!\n Спеши подписаться на самые свежие товары со скидкой!\n Официальный интернет-магазин в России: http://www.adidas.ru/'
for subscriber in allSubscribers:
    try:
        bot.send_message(str(subscriber), TEXT)
    except:
        continue
