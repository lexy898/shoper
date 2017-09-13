import telebot
import logging
import config
from telebot import types
import sql_requests


logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')

TOKEN = config.get_token()
CHAT_ID = 158041048

bot = telebot.TeleBot(TOKEN)
brands = sql_requests.get_brands()
types_of_good = sql_requests.get_types_of_good()

# Домашний экран
def set_home_screen(message):
    markup = types.ReplyKeyboardMarkup()
    markup.row('Мои подписки', 'Бренды')
    markup.row('🚫')
    bot.send_message(message.chat.id, "😌Выбирай:", reply_markup=markup)

# Экран выбора типа вещей конкретного бренда
def set_brand_settings_screen(message):
    types_of_good_by_company = sql_requests.get_ids_types_of_good_by_company(message.text)
    types_of_good_by_user = sql_requests.get_types_of_good_by_user(message.chat.id, message.text)
    subscribes = list(set(types_of_good_by_company).difference(types_of_good_by_user))
    markup = types.ReplyKeyboardMarkup()
    for subscribe in subscribes:
        markup.row("☑Подписаться на " + types_of_good[subscribe])
    for type in types_of_good_by_user:
        markup.row("✅Отписаться от " + types_of_good[type])
    markup.row(" 🔙 ")
    bot.send_message(message.chat.id, "😌Выбирай:", reply_markup=markup)

# Обновление экрана выбора типа вещей конкретного бренда
def refresh_brand_settings_screen(message):
    try:
        current_company = sql_requests.get_current_company_by_user(message.chat.id)
        types_of_good_by_company = sql_requests.get_ids_types_of_good_by_company(brands[current_company])
        types_of_good_by_user = sql_requests.get_types_of_good_by_user(message.chat.id, brands[current_company])
        subscribes = list(set(types_of_good_by_company).difference(types_of_good_by_user))
        sql_requests.set_flag_by_user(message.chat.id, brands.get(current_company))
        markup = types.ReplyKeyboardMarkup()
        for subscribe in subscribes:
            markup.row("☑Подписаться на " + types_of_good[subscribe])
        for type in types_of_good_by_user:
            markup.row("✅Отписаться от " + types_of_good[type])
        markup.row("🔙")
        bot.send_message(message.chat.id, "😌Выбирай:", reply_markup=markup)
    except:
        set_home_screen(message)

# Экран выбора бренда
def set_brands_screen(message):
    users_brands = sql_requests.get_users_brands(message.chat.id)
    list_brands = list(brands.keys())
    subscribe = list(set(list_brands).difference(users_brands))
    markup = types.ReplyKeyboardMarkup()
    for i in range(len(subscribe)):
        markup.row("☑Подписаться на " + brands[subscribe[i]])
    for i in range(len(users_brands)):
        markup.row("✅Отписаться от " + brands[users_brands[i]])
    markup.row("🏠")
    bot.send_message(message.chat.id, "😌Выбирай бренд:", reply_markup=markup)

# Экран выбора бренда из своих подписок
def set_my_subscriptions_screen(message):
    sql_requests.reset_flag_by_user(message.chat.id)  # сброс флага текущего бренда у пользователя
    subscriptions = sql_requests.get_subscriptions(message.chat.id)
    markup = types.ReplyKeyboardMarkup()
    for i in range(len(subscriptions)):
        markup.row(subscriptions[i])
    markup.row("🏠")
    bot.send_message(message.chat.id, "✔Твои подписки:", reply_markup=markup)

def subscribe(message):
    key = message.text[16:]
    if key in brands.values():
        sql_requests.add_subscribe_brand(message.chat.id, key)
        bot.send_message(message.chat.id, "Подписка на " + key + " добавлена!\n "
                                                                 "Настроить подписку можно в разделе \"Мои подписки\"")
        set_brands_screen(message)
    elif key in types_of_good.values():
        sql_requests.add_subscribe_type_of_goods(message.chat.id, key)
        bot.send_message(message.chat.id, "Подписка на " + key + " добавлена!")
        refresh_brand_settings_screen(message)

def unsubscribe(message):
    key = message.text[15:]
    if key in brands.values():
        sql_requests.del_subscribe_brand(message.chat.id, key)
        bot.send_message(message.chat.id, "Подписка на " + key + " отменена💔")
        set_brands_screen(message)
    elif key in types_of_good.values():
        sql_requests.del_subscribe_type_of_goods(message.chat.id, key)
        bot.send_message(message.chat.id, "Подписка на " + key + " отменена💔")
        refresh_brand_settings_screen(message)

@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    set_home_screen(message)

@bot.message_handler(commands=['exit'])
def handle_start_help(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, "Пока 😜", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "Мои подписки":
        set_my_subscriptions_screen(message)
    elif message.text == "Бренды":
        set_brands_screen(message)
    elif message.text == "🔙":
        set_my_subscriptions_screen(message)
    elif message.text in brands.values():    #если сообщение равно значению одного из брендов
        sql_requests.reset_flag_by_user(message.chat.id)
        sql_requests.set_flag_by_user(message.chat.id, message.text)
        set_brand_settings_screen(message)
    elif "Подписаться на" in message.text:
        subscribe(message)
    elif "Отписаться от" in message.text:
        unsubscribe(message)
    elif message.text == "🏠":
        set_home_screen(message)
    elif message.text == "🚫":
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, "Пока 😜", reply_markup=markup)
    else:
        set_home_screen(message)

@bot.message_handler(commands=['chatID'])
def handle_start_help(message):
    bot.send_message(message.chat.id, message.chat.id)

bot.polling(none_stop=True, interval=0)