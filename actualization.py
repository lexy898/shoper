import parserHnM
import parserRoxy
from datetime import datetime
import sqlRequests

def actualThings(company):
    things = sqlRequests.getThingsWithDate(company)
    counter = 0
    now = datetime.now()
    for thing in things:
        loadedDate = datetime.strptime(thing[1], "%Y-%m-%d %H:%M:%S")
        delta = now - loadedDate
        if delta.days >=7:
            if company == 'H&M':
                if not parserHnM.getThingStatusById(thing[0]):
                    sqlRequests.deleteThingById(thing[0])
                    counter +=1
            elif company == 'Roxy':
                if not parserRoxy.getThingStatusById(thing[0]):
                    sqlRequests.deleteThingById(thing[0])
                    counter +=1
    writeProtocol(str(datetime.now()) +" -------------Удалено "+str(counter)+" Вещей\n")
    print("Удалено "+str(counter)+" Вещей")

def writeProtocol(text):
    file = open('protocol.txt', 'a')
    file.write(text)
    file.close()

actualThings('H&M')
actualThings('Roxy')