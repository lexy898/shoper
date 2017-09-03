import configparser

conf = configparser.RawConfigParser()
conf.read("config.properties")

def getToken():
    return conf.get("telegramBot", "token")

def getUpdateStatus(company):
    return conf.get("update", company)

def getDaysActualization():
    return conf.get("daysActualization", "days")

def getNotifyStatus(company):
    return conf.get("notify", company)

def getProductPage(company):
    return conf.get("productPage", company)