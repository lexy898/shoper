import telebot
from telebot import util
import sql_requests

TOKEN = "426617203:AAHqKOH-62wRF1XSEFR8NS6372nHMWNR0BE"
bot = telebot.TeleBot(TOKEN)
allSubscribers = sql_requests.get_all_subscribers()
print(allSubscribers)
TEXT = '🌈Появился новый магазин ROXY!\n Спеши подписаться на самые свежие товары со скидкой!\n Официальный интернет-магазин в России: http://www.roxy-russia.ru/'
for subscriber in allSubscribers:
    bot.send_message(str(subscriber), TEXT)