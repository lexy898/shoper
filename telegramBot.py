import telebot
import logging
from telebot import types
import sqlRequests


logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')

token = "426617203:AAHqKOH-62wRF1XSEFR8NS6372nHMWNR0BE"
chat_id = 158041048

bot = telebot.TeleBot(token)

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
            brands = sqlRequests.getBrands()
            markup = types.ReplyKeyboardMarkup()
            for i in range(len(brands)):
                print(brands[i])
                markup.row(brands[i])
            bot.send_message(message.chat.id, "Choose one brand:", reply_markup=markup)

        elif message.text == "🚫":
            markdown = types.ReplyKeyboardRemove(selective=False)
            bot.send_message(message.chat.id, "Пока 😜", reply_markup=markdown)
        else:
            bot.send_message(message.chat.id, "Не понимаю, что ты мне хочешь сказать")

@bot.message_handler(commands=['chatID'])
def handle_start_help(message):
    bot.send_message(message.chat.id, message.chat.id)

bot.polling(none_stop=True, interval=0)

def view_brand_menu(chatid):
