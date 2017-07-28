import sqlite3
import logging
import httpRequests

logging.basicConfig(format = u'%(levelname)-8s [%(asctime)s] %(message)s', level = logging.ERROR, filename = u'log.txt')
_DB_PATH = "h&m.sqlite"


def saveThings(results):
    try:
        conn = sqlite3.connect(_DB_PATH)
        cursor = conn.cursor()
        for i in range(len(results)):
            thing = results[i]

            print(str(i)+"INSERT INTO result VALUES (\'"
                  +thing["defaultCode_string"]+"\',"
                  +str(thing["productWhitePrice_rub_double"])+","
                  +str(thing["actualPrice_rub_double"])+",\'"
                  +thing["name_text_ru"]+"\')")
            cursor.execute("INSERT INTO result VALUES (\""
                  +thing["defaultCode_string"]+"\","
                  +str(thing["productWhitePrice_rub_double"])+","
                  +str(thing["actualPrice_rub_double"])+",\""
                  +thing["name_text_ru"]+"\")")
        conn.commit()
        conn.close()
    except sqlite3.DatabaseError as err:
        print("Error: ", err)

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
