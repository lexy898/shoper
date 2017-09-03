import parserHnM
import parserRoxy
import parserDC
import parserQuickSilver
from datetime import datetime
import sqlRequests
import config

def actualThings(company):
    things = sqlRequests.getThingsWithDate(company)
    counter = 0
    now = datetime.now()
    for thing in things:
        loadedDate = datetime.strptime(thing[1], "%Y-%m-%d %H:%M:%S")
        delta = now - loadedDate
        if delta.days >= int(config.getDaysActualization()):
            if company == 'H&M':
                if not parserHnM.getThingStatusById(thing[0]):
                    sqlRequests.deleteThingById(thing[0])
                    counter +=1
            elif company == 'Roxy':
                if not parserRoxy.getThingStatusById(thing[0]):
                    sqlRequests.deleteThingById(thing[0])
                    counter +=1
            elif company == 'DC':
                if not parserDC.getThingStatusById(thing[0]):
                    sqlRequests.deleteThingById(thing[0])
                    counter +=1
            elif company == 'QuickSilver':
                if not parserQuickSilver.getThingStatusById(thing[0]):
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
actualThings('DC')
actualThings('QuickSilver')