from datetime import datetime

import config
import sql_requests
from parsers import parser_DC, parser_Roxy, parser_HnM, parser_QuickSilver, parser_Adidas, parser_Nike

companies_dict = {
    'H&M': parser_HnM.ParserHnM(),
    'Roxy': parser_Roxy.ParserRoxy(),
    'QuickSilver': parser_QuickSilver.ParserQuickSilver(),
    'DC': parser_DC.ParserDC(),
    'Adidas': parser_Adidas.ParserAdidas(),
    'Nike': parser_Nike.ParserNike()
}

def actual_things():
    now = datetime.now()
    for company in companies_dict:
        print(company)
        counter = 0  # Счетчик удаленных вещей
        parser = companies_dict.get(company)
        things = sql_requests.get_things_with_date(company)
        print('Вещей в БД для компании: '+str(len(things)))
        for thing in things:
            loaded_date = datetime.strptime(thing[1], "%Y-%m-%d %H:%M:%S")
            delta = now - loaded_date
            if delta.days >= int(config.get_days_actualization()):
                if not parser.get_thing_status_by_id(thing[0]):
                    print('К удалению --------'+str(thing[0]))
                    sql_requests.delete_thing_by_id(thing[0])
                    counter += 1
        write_protocol(str(datetime.now()) + "COMPANY: "+str(company)+" -------------Удалено " + str(counter) + " Вещей\n")

def write_protocol(text):
    file = open('protocol.txt', 'a')
    file.write(text)
    file.close()

actual_things()