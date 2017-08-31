import parserHnM
import sqlRequests

'''
things = parserHnM.getChildrens()
sqlRequests.saveThings(things)

things = parserHnM.getFemale()
sqlRequests.saveThings(things)

things = parserHnM.getMale()
sqlRequests.saveThings(things)

things = parserHnM.getHOME()
sqlRequests.saveThings(things)

'''
old_things = sqlRequests.getThings('H&M')
print(len(old_things))