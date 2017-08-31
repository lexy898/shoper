import sqlite3
import logging
from datetime import datetime

logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.ERROR, filename = u'log.txt')
_DB_PATH = "h&m.sqlite"


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

def deleteThingById(id):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM result WHERE defaultCode_string = \""+str(id)+"\"")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        print("Error: ", err)

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

def setHeaders(company, headers):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE header SET headers = \""+headers+"\" WHERE company = \""+company+"\"")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')

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

def setCookies(company, cookie):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE header SET cookie = \""+cookie+"\" WHERE company = \""+company+"\"")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')

def convertToDict(obj):
    import ast
    try:
        return ast.literal_eval(obj[0][0])
    except:
        import sys
        logging.error(u'Error converting to dictionary. Module: '+str(sys.modules[__name__])+'')

def getBrands(): #Возвращает бренды в виде словаря {id:brand}
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

def getBrandsInvert(): #Возвращает те же пары, что и getBrands(), но ключ и значение поменяны местами
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

def getSubscriptions(chatId): #получить названия брендов, на которые подписан пользователь
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

def getTypesOfGood():
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, description FROM type_of_goods")
        typesOfGood = cursor.fetchall()
        result = {}
        for i in range(len(typesOfGood)):
            result[typesOfGood[i][0]] = typesOfGood[i][1]
        conn.close()
        return result
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')

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

def getTypesOfGoodByCompany(company):
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

def addSubscribeBrand(chatid, brand):
    typesOfGood = getTypesOfGoodByCompany(brand)
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

def addSubscribeTypeOfGoods(chatid, typeOfGood):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO compilance_user_prod (chatid, type_of_good, company) "
                       "VALUES ("+str(chatid)+", (SELECT id FROM type_of_goods "
                                             "WHERE description = '"+str(typeOfGood)+"'),"
                       "(SELECT company FROM compilance_user_prod WHERE "
                       "chatid = "+str(chatid)+" AND flag = 1))")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')

def delSubscribeTypeOfGoods(chatid, typeOfGood):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM  compilance_user_prod WHERE "
                       "chatid = '"+str(chatid)+"' AND type_of_good = "
                       "(SELECT id FROM type_of_goods "
                       "WHERE description = '"+str(typeOfGood)+"') AND flag = 1")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')

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

def resetFlagByUser(chatid):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE compilance_user_prod SET flag = null WHERE chatid = '"+str(chatid)+"'")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')

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

def getSubscribers(brand, typeOfGood): #Получить подписчиков по бренду и типу товара
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

def getAllSubscribers(): #Получить всех подписчиков
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