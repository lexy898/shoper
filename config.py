import configparser
import os
import logging

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')

conf = configparser.RawConfigParser()
conf.read(str(os.getcwd())+"/config.properties")

def get_token():
    try:
        return conf.get("telegramBot", "token")
    except configparser.NoSectionError as err:
        logging.error(u'' + str(err) + '')

def get_update_status(company):
    try:
        return conf.get("update", company)
    except configparser.NoSectionError as err:
        logging.error(u'' + str(err) + '')

def get_days_actualization():
    try:
        return conf.get("daysActualization", "days")
    except configparser.NoSectionError as err:
        logging.error(u'' + str(err) + '')

def get_notify_status(company):
    try:
        return conf.get("notify", company)
    except configparser.NoSectionError as err:
        logging.error(u'' + str(err) + '')

def get_timeout():
    try:
        return float(conf.get("timeout", "timeout"))
    except configparser.NoSectionError as err:
        logging.error(u'' + str(err) + '')
