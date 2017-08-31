import parserHnM
import parserRoxy
import sqlRequests
import notifier
from datetime import datetime

HnMupd = False
RoxyUpd = True

def thingsUpdate(type, company):
    old_things = sqlRequests.getThings(company)
    loaded_things = []
    if company == 'H&M':
        loaded_things = getHnMLoadedResults(type)
    elif company == 'Roxy':
        loaded_things = getRoxyLoadedResults(type)
    else:
        print("Компании " + str(company) + " не существует")
        return 0
    loaded_things_codes = []
    for thing in loaded_things:
        loaded_things_codes.append(thing[0])
    print("Старые вещи: "+ str(len(old_things))+" шт.")
    writeProtocol(str(datetime.now())+" Старые вещи: "+ str(len(old_things))+" шт.\n")
    print("Загружено: "+ str(len(loaded_things_codes))+" шт.")
    writeProtocol(str(datetime.now()) + " Загружено: "+ str(len(loaded_things_codes))+" шт.\n")
    new_things_codes = list(set(loaded_things_codes).difference(old_things))
    print("Новых: "+ str(len(new_things_codes))+" шт.")
    writeProtocol(str(datetime.now()) + " Новых: "+ str(len(new_things_codes))+" шт.\n")
    new_things_codes = list(set(new_things_codes)) #Убираем дублированные элементы
    print("Новых без дублей: " + str(len(new_things_codes)) + " шт.")
    writeProtocol(str(datetime.now()) + " Новых без дублей: " + str(len(new_things_codes)) + " шт.\n")
    new_things_codes_full = new_things_codes[:] #Эти коды будут записаны в БД

    '''
    По каждому коду в списке проверяется актуальность вещи
    Если parserHnM.getThingStatusById() возвращает Fаlse,
    то код удаляется из списка
    '''
    i = 0
    while i < len(new_things_codes):
        status = False
        if company == 'H&M':
            status = parserHnM.getThingStatusById(new_things_codes[i])
        elif company == 'Roxy':
            status = parserRoxy.getThingStatusById(new_things_codes[i])
        if not status:
            del new_things_codes[i]
        else:
            i += 1
    print("Новых актуальных: " + str(len(new_things_codes)) + " шт.")
    '''
    Из всех загруженных вещей записываем в БД только те, 
    коды которых имеются в списке "new_things_codes_full"
    '''
    new_things = [] #Список будет содержать полные записи новых вещей
    for loaded_thing in loaded_things:
        if (new_things_codes_full.count(loaded_thing[0]) != 0):
            new_things.append(loaded_thing)
    sqlRequests.addNewThings(new_things, company)

    '''
    Убираем из new_things все вещи, которые е прошли проверку на актуальность
    '''
    i = 0
    while i < len(new_things):
        if new_things_codes.count(new_things[i][0]) == 0:
            del new_things[i]
        else:
            i += 1

    return new_things

def writeProtocol(text):
    file = open('protocol.txt', 'a')
    file.write(text)
    file.close()

def getHnMLoadedResults(type):
    loaded_results = []
    if type == 'male':
        loaded_results = parserHnM.getMale()
    elif type == 'female':
        loaded_results = parserHnM.getFemale()
    elif type == 'childrens':
        loaded_results = parserHnM.getChildrens()
    elif type == 'HOME':
        loaded_results = parserHnM.getHOME()
    else:
        print("Параметра " + str(type) + " не существует")
    return loaded_results

def getRoxyLoadedResults(type):
    loaded_results = []
    if type == 'female':
        loaded_results = parserRoxy.getFemale()
    elif type == 'childrens':
        loaded_results = parserRoxy.getChildrens()
    else:
        print("Параметра " + str(type) + " не существует")
    return loaded_results

def notify(new_things, type):
    print("Type: "+type+", Добавлено штук:"+str(len(new_things)))
    if len(new_things) != 0:
        notifier.sendMessageHnM(new_things, type)

if HnMupd:
    types = ['male','female','childrens','HOME']
    for type in types:
        new_things = thingsUpdate(type,'H&M')
        #notify(new_things, types[i])

if RoxyUpd:
    types = ['female','childrens']
    for type in types:
        new_things = thingsUpdate(type,'Roxy')
        #notify(new_things, types[i])