import parserHnM
import sqlRequests
from datetime import datetime

now = datetime.now()
print(now)
loadedDate = datetime.strptime("2017-08-22 23:08:54", "%Y-%m-%d %H:%M:%S")
print(loadedDate)
delta = loadedDate - now
delta.days
print(delta.days)
print(type(delta))


things = parserHnM.getChildrens()
sqlRequests.saveThings(things)

things = parserHnM.getFemale()
sqlRequests.saveThings(things)

things = parserHnM.getMale()
sqlRequests.saveThings(things)

things = parserHnM.getHOME()
sqlRequests.saveThings(things)


