import parser_HnM
import parser_Roxy
import parser_DC
import parser_QuickSilver
from datetime import datetime
import sql_requests
import config

def actual_things(company):
    things = sql_requests.get_things_with_date(company)
    counter = 0
    now = datetime.now()
    for thing in things:
        loaded_date = datetime.strptime(thing[1], "%Y-%m-%d %H:%M:%S")
        delta = now - loaded_date
        if delta.days >= int(config.get_days_actualization()):
            if company == 'H&M':
                if not parser_HnM.get_thing_status_by_id(thing[0]):
                    sql_requests.delete_thing_by_id(thing[0])
                    counter +=1
            elif company == 'Roxy':
                if not parser_Roxy.get_thing_status_by_id(thing[0]):
                    sql_requests.delete_thing_by_id(thing[0])
                    counter +=1
            elif company == 'DC':
                if not parser_DC.get_thing_status_by_id(thing[0]):
                    sql_requests.delete_thing_by_id(thing[0])
                    counter +=1
            elif company == 'QuickSilver':
                if not parser_QuickSilver.get_thing_status_by_id(thing[0]):
                    sql_requests.delete_thing_by_id(thing[0])
                    counter +=1
    write_protocol(str(datetime.now()) + " -------------Удалено " + str(counter) + " Вещей\n")
    print("Удалено "+str(counter)+" Вещей")

def write_protocol(text):
    file = open('protocol.txt', 'a')
    file.write(text)
    file.close()

actual_things('H&M')
actual_things('Roxy')
actual_things('DC')
actual_things('QuickSilver')