import sqlite3
import logging
from datetime import datetime
import os

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')
_DB_PATH = str(os.getcwd())+"/h&m.sqlite"


# Добавить новые вещи в БД
def add_new_things(new_things, company):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM COMPANY WHERE company_name ='" + str(company) + "'")
        company = cursor.fetchone()[0]
        for thing in new_things:
            print("INSERT INTO result VALUES (\""
                           + str(thing[0]) + "\","
                           + str(thing[1]) + ","
                           + str(thing[2]) + ", \""
                           + str(thing[3]).replace('"', '') + "\", \""
                           + str(thing[4]).replace('"', '') + "\","
                           + str(company) + ", \""
                           + datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S") + "\", \""
                           + str(thing[5]) + "\", \""
                           + str(thing[6]) + "\")")
            cursor.execute("INSERT INTO result VALUES (\""
                           + str(thing[0]) + "\","
                           + str(thing[1]) + ","
                           + str(thing[2]) + ", \""
                           + str(thing[3]).replace('"', '') + "\", \""
                           + str(thing[4]).replace('"', '') + "\","
                           + str(company) + ", \""
                           + datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S") + "\", \""
                           + str(thing[5]) + "\", \""
                           + str(thing[6]) + "\")")
            conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        print("Error: ", err)


# Удалить вещь по ID
def delete_thing_by_id(id):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM result WHERE defaultCode_string = \"" + str(id) + "\"")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        print("Error: ", err)


# Получить коды вещей указанной компании
def get_things(company):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT defaultCode_string FROM result WHERE COMPANY = "
                       "(SELECT id FROM COMPANY WHERE company_name ='" + str(company) + "')")
        things = cursor.fetchall()
        result = [x[0] for x in things]
        conn.close()
        return result
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')


# Получить код вещи указанной компании с датой ее загрузки
def get_things_with_date(company):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT defaultCode_string, date FROM result WHERE COMPANY = "
                       "(SELECT id FROM COMPANY WHERE company_name ='" + str(company) + "')")
        result = cursor.fetchall()
        conn.close()
        return result
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')


# Получить http заголовки интернет-магазина
def get_headers(company):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT headers FROM header WHERE COMPANY = \"" + company + "\"")
        headers = cursor.fetchall()
        conn.close()
        return convert_to_dict(headers)
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')


# Записать http заголовки интернет-магазина
def set_headers(company, headers):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE header SET headers = \"" + headers + "\" WHERE COMPANY = \"" + company + "\"")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')


# Получить cookies  интернет-магазина
def get_cookies(company):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT cookie FROM header WHERE COMPANY = \"" + company + "\"")
        cookies = cursor.fetchall()
        conn.close()
        return convert_to_dict(cookies)
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')


# Записать cookies  интернет-магазина
def set_cookies(company, cookie):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE header SET cookie = \"" + cookie + "\" WHERE COMPANY = \"" + company + "\"")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')


# преобразовать в словарь
def convert_to_dict(obj):
    import ast
    try:
        return ast.literal_eval(obj[0][0])
    except:
        import sys
        logging.error(u'Error converting to dictionary. Module: ' + str(sys.modules[__name__]) + '')


# Возвращает бренды в виде словаря {id:brand}
def get_brands():
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, company_name FROM COMPANY")
        brands = cursor.fetchall()
        result = {}
        for i in range(len(brands)):
            result[brands[i][0]] = brands[i][1]
        conn.close()
        return result
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')


# Возвращает те же пары, что и get_brands(), но ключ и значение поменяны местами
def get_brands_invert():
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT company_name, id FROM COMPANY")
        brands = cursor.fetchall()
        result = {}
        for i in range(len(brands)):
            result[brands[i][0]] = brands[i][1]
        conn.close()
        return result
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')


# получить названия брендов, на которые подписан пользователь
def get_subscriptions(chatId):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT c.company_name FROM COMPANY c "
                       "INNER JOIN compilance_user_prod cup ON cup.COMPANY = c.id "
                       "WHERE cup.chatid = '" + str(chatId) + "'")
        subscriptions = cursor.fetchall()
        result = [x[0] for x in subscriptions]
        conn.close()
        return result
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')


# Получить словарь id:  description (содержит типы вещей)
def get_types_of_good():
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, description FROM type_of_goods")
        typesOfGood = cursor.fetchall()
        result = {}
        for type in typesOfGood:
            result[type[0]] = type[1]
        conn.close()
        return result
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')


# Получить список id типов вещей
def get_id_types_of_good_by_type(type):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM type_of_goods WHERE type = \'" + type + "\'")
        id_of_good = cursor.fetchone()
        conn.close()
        result = id_of_good[0]
        return result
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')


# Получить текущий активный бренд конкретного пользователя
def get_current_company_by_user(chatId):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT COMPANY FROM compilance_user_prod "
                       "WHERE chatid = '" + str(chatId) + "' AND flag = 1")
        current_company = cursor.fetchall()
        result = current_company[0][0]
        return result
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')


# Получить id типов вещей указанной компании
def get_ids_types_of_good_by_company(company):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT type_of_good FROM compilance_comp_prod "
                       "WHERE company_id = (SELECT id FROM COMPANY "
                       "WHERE company_name = '" + str(company) + "')")
        types_of_good = cursor.fetchall()
        result = [x[0] for x in types_of_good]
        conn.close()
        return result
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')


# Получить Названия типов вещей указанной компании
def get_types_of_good_by_company(company):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT TOG.type FROM compilance_comp_prod CCP "
                       "JOIN type_of_goods TOG ON CCP.type_of_good = TOG.id "
                       "WHERE company_id = (SELECT id FROM COMPANY WHERE company_name = \'" + company + "\')")
        types_of_good = cursor.fetchall()
        result = [x[0] for x in types_of_good]
        conn.close()
        return result
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')


# Получить список типов вещей конкретного пользователя для указанного бренда
def get_types_of_good_by_user(chatid, company):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT type_of_good FROM compilance_user_prod "
                       "WHERE COMPANY = (SELECT id FROM COMPANY "
                       "WHERE company_name = '" + str(company) + "') "
                                                                 "AND chatid = '" + str(chatid) + "'")
        types_of_good = cursor.fetchall()
        result = [x[0] for x in types_of_good]
        conn.close()
        return result
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')


# Добавить подписку на бренд для конкретного пользователя
def add_subscribe_brand(chatid, brand):
    types_of_good = get_ids_types_of_good_by_company(brand)
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id from COMPANY WHERE company_name = '" + brand + "'")
        id = cursor.fetchall()
        id = id[0][0]
        for i in range(len(types_of_good)):
            cursor.execute("INSERT INTO compilance_user_prod (chatid, type_of_good, COMPANY) "
                           "VALUES ('" + str(chatid) + "'," + str(types_of_good[i]) + ", " + str(id) + ")")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')


# Удалить подписку от бренда для конкретного пользователя
def del_subscribe_brand(chatid, brand):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id from COMPANY WHERE company_name = '" + brand + "'")
        id_of_company = cursor.fetchall()
        id_of_company = id_of_company[0][0]
        cursor.execute("DELETE FROM compilance_user_prod WHERE chatid = '" + str(chatid) + "' AND COMPANY = " + str(id_of_company))
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')


# Добавить подписку на тип вещи текущего бренда для конкретного пользователя
def add_subscribe_type_of_goods(chatid, typeOfGood):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO compilance_user_prod (chatid, type_of_good, COMPANY) "
                       "VALUES (" + str(chatid) + ", (SELECT id FROM type_of_goods "
                                                  "WHERE description LIKE '%" + str(typeOfGood) + "%'),"
                                                                                                  "(SELECT COMPANY FROM compilance_user_prod WHERE "
                                                                                                  "chatid = " + str(
            chatid) + " AND flag = 1))")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')


# Удалить подписку с типа вещи конкретного пользователя текущего бренда
def del_subscribe_type_of_goods(chatid, typeOfGood):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM  compilance_user_prod WHERE "
                       "chatid = '" + str(chatid) + "' AND type_of_good = "
                                                    "(SELECT id FROM type_of_goods "
                                                    "WHERE description LIKE '%" + str(typeOfGood) + "%') AND flag = 1")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')


# Получить id всех брендов, на которые подписан пользователь
def get_users_brands(chatid):  # Получить id всех брендов, на которые подписан пользователь
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT COMPANY FROM compilance_user_prod "
                       "WHERE chatid = '" + str(chatid) + "'")
        users_brands = cursor.fetchall()
        result = [x[0] for x in users_brands]
        conn.close()
        return result
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')


# Снять все флаги активного бренда конкретного пользователя
def reset_flag_by_user(chatid):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE compilance_user_prod SET flag = null WHERE chatid = '" + str(chatid) + "'")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')


# Установить флаг активного бренда конкретного пользователя
def set_flag_by_user(chatid, company):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE compilance_user_prod SET flag = 1 WHERE chatid = '" + str(chatid) + "' "
                                                                                                   "AND COMPANY = (SELECT id FROM COMPANY WHERE company_name = '" + company + "')")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')


# Получить подписчиков по бренду и типу товара
def get_subscribers(brand, type_of_good):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT chatid FROM compilance_user_prod "
                       "WHERE COMPANY = '" + str(brand) + "' AND type_of_good = '" + str(type_of_good) + "'")
        subscribers = cursor.fetchall()
        conn.close()
        result = [x[0] for x in subscribers]
        return result
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')


# Получить всех подписчиков
def get_all_subscribers():
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT chatid FROM compilance_user_prod")
        subscribers = cursor.fetchall()
        conn.close()
        result = [x[0] for x in subscribers]
        return result
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')


# Получить Description конкретного типа вещи
def get_description_by_type_of_good(type):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT description FROM type_of_goods WHERE type = \'" + type + "\'")
        description = cursor.fetchone()
        conn.close()
        result = description[0]
        return result
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')

def get_link_by_id(thing_id):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT link FROM result WHERE defaultCode_string = \'" + str(thing_id) + "\'")
        link = cursor.fetchone()
        conn.close()
        return link[0]
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')
    except TypeError as err:
        logging.error(u'' + str(err) + '')
        return ''

