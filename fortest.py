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
new_things_codes = ['1',2,3,4,5,'6',7,8,9,1,2,3,4,5,'6','6','6','6','6',7,8,9]
print(new_things_codes)
new_things_codes = list(set(new_things_codes))
print(new_things_codes)
