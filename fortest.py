import parserHnM
import sqlRequests

things = parserHnM.getHOME()
sqlRequests.saveThings(things)
