from datetime import datetime
import logging
import config
import notifier
import sql_requests
from parsers import parser_Adidas, parser_DC, parser_Roxy, parser_HnM, parser_QuickSilver, parser_Nike

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')
companies_dict = {
    'H&M': parser_HnM.ParserHnM(),
    'Roxy': parser_Roxy.ParserRoxy(),
    'QuickSilver': parser_QuickSilver.ParserQuickSilver(),
    'DC': parser_DC.ParserDC(),
    'Adidas': parser_Adidas.ParserAdidas(),
    'Nike': parser_Nike.ParserNike()
}

def things_update(type, company):
    old_things = sql_requests.get_things(company)
    loaded_things = []
    parser = companies_dict.get(company)
    loaded_things = parser.get_loaded_results(type)
    loaded_things_codes = []
    for thing in loaded_things:
        loaded_things_codes.append(thing[0])
    write_protocol("Старые вещи: " + str(len(old_things)) + " шт.\n")
    write_protocol("Загружено: " + str(len(loaded_things_codes)) + " шт.\n")
    new_things_codes = list(set(loaded_things_codes).difference(old_things))
    write_protocol("Новых: " + str(len(new_things_codes)) + " шт.\n")
    new_things_codes_full = new_things_codes[:]  # Эти коды будут записаны в БД
    write_protocol('____________________\n\n')

    '''
    Из всех загруженных вещей записываем в БД только те, 
    коды которых имеются в списке "new_things_codes_full"
    '''
    new_things = []  # Список будет содержать полные записи новых вещей
    for loaded_thing in loaded_things:
        if new_things_codes_full.count(loaded_thing[0]) != 0:
            new_things.append(loaded_thing)
            new_things_codes_full.remove(
                loaded_thing[0])  # Удаляется из списка для предотвращения отправки возможных дублей
    sql_requests.add_new_things(new_things, company)

    '''
    Убираем из new_things все неактуальные вещи
    '''
    for new_thing in new_things:
        # Если статус равен False, то вещь удаляется из списка
        if not new_thing[6]:
            try:
                new_things.remove(new_thing)
            except ValueError as err:
                logging.error(u'' + str(err) + '' )
    return new_things


def write_protocol(text):
    file = open('protocol.txt', 'a')
    file.write(text)
    file.close()


def notify(new_things, type, company):
    print("Type: " + type + ", Добавлено штук:" + str(len(new_things)))
    if len(new_things) != 0:
        notifier.send_message(new_things, type, company)


brands = sql_requests.get_brands_invert().keys()
for brand in brands:
    if config.get_update_status(brand) == 'True':
        write_protocol('******* COMPANY: ' + brand + ' | time: ' + str(datetime.now()) + ' *******\n')
        types = sql_requests.get_types_of_good_by_company(brand)
        for type in types:
            try:
                write_protocol('******* type: ' + type + '\n')
                new_things = things_update(type, brand)
                if config.get_notify_status(brand) == 'True':
                    notify(new_things, type, brand)
                write_protocol('______________________________________\n\n')
            except:
                continue
