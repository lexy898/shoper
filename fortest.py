import parserHnM
import sqlRequests

things = parserHnM.getChildrens()
sqlRequests.saveThings(things)

things = parserHnM.getFemale()
sqlRequests.saveThings(things)

things = parserHnM.getMale()
sqlRequests.saveThings(things)

things = parserHnM.getHOME()
sqlRequests.saveThings(things)


