import telebot
import logging
from telebot import types
import sqlRequests


logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')

token = "426617203:AAHqKOH-62wRF1XSEFR8NS6372nHMWNR0BE"
chat_id = 158041048

bot = telebot.TeleBot(token)
brands = sqlRequests.getBrands()
typesOfgood = sqlRequests.getTypesOfGood()

def setHomeScreen(message):
    markup = types.ReplyKeyboardMarkup()
    markup.row('Мои подписки', 'Бренды')
    markup.row('🚫')
    bot.send_message(message.chat.id, "🖖", reply_markup=markup)

def setBrandSettingsScreen(message):
    typesOfGoodByCompany = sqlRequests.getTypesOfGoodByCompany(message.text)
    typesOfGoodByUser = sqlRequests.getTypesOfGoodByUser(message.chat.id, message.text)
    subscribe = list(set(typesOfGoodByCompany).difference(typesOfGoodByUser))
    markup = types.ReplyKeyboardMarkup()
    for i in range(len(subscribe)):
        markup.row("✅Подписаться на " + typesOfgood[subscribe[i]])
    for i in range(len(typesOfGoodByUser)):
        markup.row("❌Отписаться от " + typesOfgood[typesOfGoodByUser[i]])
    markup.row("🏠")
    bot.send_message(message.chat.id, "Choose:", reply_markup=markup)

def refreshBrandSettingsScreen(message):
    try:
        currentCompany = sqlRequests.getCurrentCompanyByUser(message.chat.id)
        typesOfGoodByCompany = sqlRequests.getTypesOfGoodByCompany(brands[currentCompany])
        typesOfGoodByUser = sqlRequests.getTypesOfGoodByUser(message.chat.id, brands[currentCompany])
        subscribe = list(set(typesOfGoodByCompany).difference(typesOfGoodByUser))
        markup = types.ReplyKeyboardMarkup()
        for i in range(len(subscribe)):
            markup.row("✅Подписаться на " + typesOfgood[subscribe[i]])
        for i in range(len(typesOfGoodByUser)):
            markup.row("❌Отписаться от " + typesOfgood[typesOfGoodByUser[i]])
        markup.row("🏠")
        bot.send_message(message.chat.id, "Choose:", reply_markup=markup)
    except:
        setHomeScreen(message)

def setBrandsScreen(message):
    usersBrands = sqlRequests.getUsersBrands(message.chat.id)
    listBrands = list(brands.keys())
    subscribe = list(set(listBrands).difference(usersBrands))
    markup = types.ReplyKeyboardMarkup()
    for i in range(len(subscribe)):
        markup.row("✅Подписаться на " + brands[subscribe[i]])
    for i in range(len(usersBrands)):
        markup.row("❌Отписаться от " + brands[usersBrands[i]])
    markup.row("🏠")
    bot.send_message(message.chat.id, "Choose one brand:", reply_markup=markup)

def setMySubscriptionsScreen(message):
    sqlRequests.resetFlagByUser(message.chat.id)  # сброс флага текущего бренда у пользователя
    subscriptions = sqlRequests.getSubscriptions(message.chat.id)
    markup = types.ReplyKeyboardMarkup()
    for i in range(len(subscriptions)):
        markup.row(subscriptions[i])
    markup.row("🏠")
    bot.send_message(message.chat.id, "Your subscriptions:", reply_markup=markup)

def subscribe(message):
    key = message.text[16:]
    if key in brands.values():
        sqlRequests.addSubscribeBrand(message.chat.id, key)
        bot.send_message(message.chat.id, "Подписка на " + key + " оформлена!\n "
                                                                 "Настроить подписку можно в разделе \"Мои подписки\"")
        setBrandsScreen(message)
    elif key in typesOfgood.values():
        sqlRequests.addSubscribeTypeOfGoods(message.chat.id, key)
        bot.send_message(message.chat.id, "Подписка на " + key + " добавлена!")
        refreshBrandSettingsScreen(message)

def unsubscribe(message):
    key = message.text[15:]
    if key in brands.values():
        sqlRequests.delSubscribeBrand(message.chat.id, key)
        bot.send_message(message.chat.id, "Подписка на " + key + " отменена💔")
        setBrandsScreen(message)
    elif key in typesOfgood.values():
        sqlRequests.delSubscribeTypeOfGoods(message.chat.id, key)
        bot.send_message(message.chat.id, "Подписка на " + key + " отменена💔")
        refreshBrandSettingsScreen(message)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    setHomeScreen(message)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "Мои подписки":
        setMySubscriptionsScreen(message)
    elif message.text == "Бренды":
        setBrandsScreen(message)
    elif list(brands.values()).count(message.text) != 0: #если сообщение равно значению одного из брендов
        sqlRequests.resetFlagByUser(message.chat.id)
        sqlRequests.setFlagByUser(message.chat.id, message.text)
        setBrandSettingsScreen(message)
    elif "Подписаться на" in message.text:
        subscribe(message)
    elif "Отписаться от" in message.text:
        unsubscribe(message)
    elif message.text == "🏠":
        setHomeScreen(message)
    elif message.text == "🚫":
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, "Пока 😜", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Не понимаю, что ты мне хочешь сказать")

@bot.message_handler(commands=['chatID'])
def handle_start_help(message):
    bot.send_message(message.chat.id, message.chat.id)

bot.polling(none_stop=True, interval=0)