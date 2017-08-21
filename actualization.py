import parserHnM
import time
import sqlRequests

def actualThingsHnM():
    things = sqlRequests.getThings()
    counter = 0
    for i in range(len(things)):
        if parserHnM.getThingStatusById(things[i]) == False:
            sqlRequests.deleteThingById(things[i])
            counter +=1
        #time.sleep(1)
    print("Удалено "+str(counter)+" Вещей")

actualThingsHnM()