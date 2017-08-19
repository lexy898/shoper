import sqlite3
import logging

logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.ERROR, filename = u'log.txt')
_DB_PATH = "h&m.sqlite"


def saveThings(results):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        for i in range(len(results)):
            thing = results[i]
            cursor.execute("INSERT INTO result VALUES (\""
                  +str(thing["defaultCode_string"])+"\","
                  +str(thing["productWhitePrice_rub_double"])+","
                  +str(thing["actualPrice_rub_double"])+",\""
                  +str(thing["name_text_ru"])+"\",\""
                  +str(thing["sizes_ru_string_mv"]) + "\")")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        print("Error: ", err)

def addNewThings(new_things):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        for i in range(len(new_things)):
            thing = new_things[i]
            cursor.execute("INSERT INTO result VALUES (\""
                  + str(thing[0]) + "\","
                  + str(thing[1]) + ","
                  + str(thing[2]) + ",\""
                  + str(thing[3]) + "\",\""
                  + str(thing[4]) + "\")")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        print("Error: ", err)

def deleteNotActualThings(not_actual_things):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        for i in range(len(not_actual_things)):
            thing = not_actual_things[i]
            print("DELETE FROM result WHERE defaultCode_string = \""+str(thing[0])+"\"")
            cursor.execute("DELETE FROM result WHERE defaultCode_string = \""+str(thing[0])+"\"")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        print("Error: ", err)

def getThings():
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT defaultCode_string FROM result")
        things = cursor.fetchall()
        result = [x[0] for x in things]
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

def getBrands():
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT company_name FROM company")
        brands = cursor.fetchall()
        result = [x[0] for x in brands]
        conn.close()
        return result
    except sqlite3.DatabaseError as err:
        logging.error(u'' + str(err) + '')