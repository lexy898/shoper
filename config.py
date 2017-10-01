import configparser
import os

conf = configparser.RawConfigParser()
conf.read(str(os.getcwd())+"/config.properties")

def get_token():
    return conf.get("telegramBot", "token")

def get_update_status(company):
    return conf.get("update", company)

def get_days_actualization():
    return conf.get("daysActualization", "days")

def get_notify_status(company):
    return conf.get("notify", company)

def get_timeout():
    return float(conf.get("timeout", "timeout"))
