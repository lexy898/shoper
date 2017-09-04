import sqlite3
import logging
from datetime import datetime

logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.ERROR, filename = u'log.txt')
_DB_PATH = "h&m.sqlite"

# Сохранить вещи в БД
def saveThings(results, company):
    default = "-"
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM company WHERE company_name ='"+str(company)+"'")
        company = cursor.fetchone()[0]
        for i in range(len(results)):
            thing = results[i]
            cursor.execute("INSERT INTO result VALUES (\""
                  +str(thing["defaultCode_string"])+"\","
                  +str(thing["productWhitePrice_rub_double"])+","
                  +str(thing["actualPrice_rub_double"])+",\""
                  +str(thing["name_text_ru"]).replace('"','')+"\",\""
                  +str(thing.get("sizes_ru_string_mv",default)) + "\", \""
                  +str(company)+","
                  +datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")+"\")")
            conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        print("Error: ", err)

# Добавить новые вещи в БД
def addNewThings(new_things, company):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM company WHERE company_name ='" + str(company) + "'")
        company = cursor.fetchone()[0]
        for thing in new_things:
            print("INSERT INTO result VALUES (\""
                  + str(thing[0]) + "\","
                  + str(thing[1]) + ","
                  + str(thing[2]) + ",\""
                  + str(thing[3]).replace('"','') + "\",\""
                  + str(thing[4]) + "\","
                  + str(company) + ",\""
                  +datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")+"\")")
            cursor.execute("INSERT INTO result VALUES (\""
                  + str(thing[0]) + "\","
                  + str(thing[1]) + ","
                  + str(thing[2]) + ",\""
                  + str(thing[3]).replace('"','') + "\",\""
                  + str(thing[4]) + "\","
                  + str(company) + ",\""
                  +datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")+"\")")
            conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        print("Error: ", err)

# Удалить вещь по ID
def deleteThingById(id):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM result WHERE defaultCode_string = \""+str(id)+"\"")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        print("Error: ", err)

# Получить коды вещей указанной компании
def getThings(company):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT defaultCode_string FROM result WHERE company = "
                       "(SELECT id FROM company WHERE company_name ='"+str(company)+"')")
        things = cursor.fetchall()
        result = [x[0] for x in things]
        conn.close()
        return result
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')

# Получить код вещи указанной компании с датой ее загрузки
def getThingsWithDate(company):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT defaultCode_string, date FROM result WHERE company = "
                       "(SELECT id FROM company WHERE company_name ='"+str(company)+"')")
        result = cursor.fetchall()
        conn.close()
        return result
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')

# Получить http заголовки интернет-магазина
def getHeaders(company):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT headers FROM header WHERE company = \""+company+"\"")
        headers = cursor.fetchall()
        conn.close()
        return convertToDict(headers)
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')

# Записать http заголовки интернет-магазина
def setHeaders(company, headers):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE header SET headers = \""+headers+"\" WHERE company = \""+company+"\"")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')

# Получить cookies  интернет-магазина
def getCookies(company):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT cookie FROM header WHERE company = \""+company+"\"")
        cookies = cursor.fetchall()
        conn.close()
        return convertToDict(cookies)
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')

# Записать cookies  интернет-магазина
def setCookies(company, cookie):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE header SET cookie = \""+cookie+"\" WHERE company = \""+company+"\"")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')

# преобразовать в словарь
def convertToDict(obj):
    import ast
    try:
        return ast.literal_eval(obj[0][0])
    except:
        import sys
        logging.error(u'Error converting to dictionary. Module: '+str(sys.modules[__name__])+'')

#Возвращает бренды в виде словаря {id:brand}
def getBrands():
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, company_name FROM company")
        brands = cursor.fetchall()
        result = {}
        for i in range(len(brands)):
            result[brands[i][0]] = brands[i][1]
        conn.close()
        return result
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')

#Возвращает те же пары, что и getBrands(), но ключ и значение поменяны местами
def getBrandsInvert():
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT company_name, id FROM company")
        brands = cursor.fetchall()
        result = {}
        for i in range(len(brands)):
            result[brands[i][0]] = brands[i][1]
        conn.close()
        return result
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')

#получить названия брендов, на которые подписан пользователь
def getSubscriptions(chatId):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT c.company_name FROM company c "
                       "INNER JOIN compilance_user_prod cup ON cup.company = c.id "
                       "WHERE cup.chatid = '"+str(chatId)+"'")
        subscriptions = cursor.fetchall()
        result = [x[0] for x in subscriptions]
        conn.close()
        return result
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')

#Получить словарь id:  description (содержит типы вещей)
def getTypesOfGood():
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
def getIdTypesOfGoodByType(type):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM type_of_goods WHERE type = \'"+type+"\'")
        id = cursor.fetchone()
        conn.close()
        result = id[0]
        return result
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')

# Получить текущий активный бренд конкретного пользователя
def getCurrentCompanyByUser(chatId):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT company FROM compilance_user_prod "
                       "WHERE chatid = '"+str(chatId)+"' AND flag = 1")
        currentCompany = cursor.fetchall()
        result = currentCompany[0][0]
        return result
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')

# Получить id типов вещей указанной компании
def getIdsTypesOfGoodByCompany(company):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT type_of_good FROM compilance_comp_prod "
                       "WHERE company_id = (SELECT id FROM company "
                       "WHERE company_name = '"+str(company)+"')")
        typesOfGood = cursor.fetchall()
        result = [x[0] for x in typesOfGood]
        conn.close()
        return result
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')

# Получить Названия типов вещей указанной компании
def getTypesOfGoodByCompany(company):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT TOG.type FROM compilance_comp_prod CCP "
                       "JOIN type_of_goods TOG ON CCP.type_of_good = TOG.id "
                       "WHERE company_id = (SELECT id FROM company WHERE company_name = \'"+company+"\')")
        typesOfGood = cursor.fetchall()
        result = [x[0] for x in typesOfGood]
        conn.close()
        return result
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')

# Получить список типов вещей конкретного пользователя для указанного бренда
def getTypesOfGoodByUser(chatid, company):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT type_of_good FROM compilance_user_prod "
                       "WHERE company = (SELECT id FROM company "
                       "WHERE company_name = '"+str(company)+"') "
                       "AND chatid = '"+str(chatid)+"'")
        typesOfGood = cursor.fetchall()
        result = [x[0] for x in typesOfGood]
        conn.close()
        return result
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')

# Добавить подписку на бренд для конкретного пользователя
def addSubscribeBrand(chatid, brand):
    typesOfGood = getIdsTypesOfGoodByCompany(brand)
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id from company WHERE company_name = '"+brand+"'")
        id = cursor.fetchall()
        id = id[0][0]
        for i in range(len(typesOfGood)):
            cursor.execute("INSERT INTO compilance_user_prod (chatid, type_of_good, company) "
                           "VALUES ('"+str(chatid)+"',"+str(typesOfGood[i])+", "+str(id)+")")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')

# Удалить подписку от бренда для конкретного пользователя
def delSubscribeBrand(chatid, brand):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id from company WHERE company_name = '"+brand+"'")
        id = cursor.fetchall()
        id = id[0][0]
        cursor.execute("DELETE FROM compilance_user_prod WHERE chatid = '"+str(chatid)+"' AND company = "+str(id))
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')

# Добавить подписку на тип вещи текущего бренда для конкретного пользователя
def addSubscribeTypeOfGoods(chatid, typeOfGood):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO compilance_user_prod (chatid, type_of_good, company) "
                       "VALUES ("+str(chatid)+", (SELECT id FROM type_of_goods "
                                             "WHERE description LIKE '%"+str(typeOfGood)+"%'),"
                       "(SELECT company FROM compilance_user_prod WHERE "
                       "chatid = "+str(chatid)+" AND flag = 1))")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')

# Удалить подписку с типа вещи конкретного пользователя текущего бренда
def delSubscribeTypeOfGoods(chatid, typeOfGood):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM  compilance_user_prod WHERE "
                       "chatid = '"+str(chatid)+"' AND type_of_good = "
                       "(SELECT id FROM type_of_goods "
                       "WHERE description LIKE '%"+str(typeOfGood)+"%') AND flag = 1")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')

# Получить id всех брендов, на которые подписан пользователь
def getUsersBrands(chatid): #Получить id всех брендов, на которые подписан пользователь
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT company FROM compilance_user_prod "
                       "WHERE chatid = '"+str(chatid)+"'")
        usersBrands = cursor.fetchall()
        result = [x[0] for x in usersBrands]
        conn.close()
        return result
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')

# Снять все флаги активного бренда конкретного пользователя
def resetFlagByUser(chatid):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE compilance_user_prod SET flag = null WHERE chatid = '"+str(chatid)+"'")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')

# Установить флаг активного бренда конкретного пользователя
def setFlagByUser(chatid, company):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE compilance_user_prod SET flag = 1 WHERE chatid = '"+str(chatid)+"' "
                        "AND company = (SELECT id FROM company WHERE company_name = '"+company+"')")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')

# Получить подписчиков по бренду и типу товара
def getSubscribers(brand, typeOfGood):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT chatid FROM compilance_user_prod "
                       "WHERE company = '"+str(brand)+"' AND type_of_good = '"+str(typeOfGood)+"'")
        subscribers = cursor.fetchall()
        conn.close()
        result = [x[0] for x in subscribers]
        return result
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')

# Получить всех подписчиков
def getAllSubscribers():
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
def getDescriptionByTypeOfGood(type):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT description FROM type_of_goods WHERE type = \'"+type+"\'")
        description = cursor.fetchone()
        conn.close()
        result = description[0]
        return result
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')

