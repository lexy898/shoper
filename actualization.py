import parserHnM
from datetime import datetime
import sqlRequests

def actualThingsHnM():
    things = sqlRequests.getThingsWithDate()
    counter = 0
    now = datetime.now()
    for i in range(len(things)):
        loadedDate = datetime.strptime(things[i][1], "%Y-%m-%d %H:%M:%S")
        delta = now - loadedDate
        if delta.days >=7:
            print(loadedDate)
            if parserHnM.getThingStatusById(things[i][0]) == False:
                sqlRequests.deleteThingById(things[i][0])
                counter +=1
    writeProtocol(str(datetime.now()) +" -------------Удалено "+str(counter)+" Вещей\n")
    print("Удалено "+str(counter)+" Вещей")

def writeProtocol(text):
    file = open('protocol.txt', 'a')
    file.write(text)
    file.close

actualThingsHnM()