import parserHnM
import sqlRequests
import notifier

HnMupd = True

def thingsUpdateHnM(type):
    old_things = sqlRequests.getThings()
    if type == 'male':
        loaded_results = parserHnM.getMale()
    elif type == 'female':
        loaded_results = parserHnM.getFemale()
    elif type == 'childrens':
        loaded_results = parserHnM.getChildrens()
    elif type == 'HOME':
        loaded_results = parserHnM.getHOME()
    else:
        print("Параметра "+str(type)+" не существует")
        return []
    loaded_things = []
    loaded_things_codes = []
    for i in range(len(loaded_results)):
        result = (loaded_results[i]["defaultCode_string"],
                  loaded_results[i]["productWhitePrice_rub_double"],
                  loaded_results[i]["actualPrice_rub_double"],
                  loaded_results[i]["name_text_ru"],
                  loaded_results[i].get("sizes_ru_string_mv","-"),)
        loaded_things.append(result)
        loaded_things_codes.append(result[0])
    print("Старые вещи: "+ str(len(old_things))+" шт.")
    print("Загружено: "+ str(len(loaded_things_codes))+" шт.")
    new_things_codes = list(set(loaded_things_codes).difference(old_things))
    print("Новых: "+ str(len(new_things_codes))+" шт.")

    '''
    По каждому коду в списке проверяется актуальность вещи
    Если parserHnM.getThingStatusById() возвращает Flse,
    то код удаляется из списка
    '''
    i = 0
    while i < len(new_things_codes):
        if parserHnM.getThingStatusById(new_things_codes[i]) == False:
            del new_things_codes[i]
        else:
            i += 1

    '''
    Из всех загруженных вещей записываем в БД только те, 
    коды которых имеются в списке "new_things_codes"
    '''
    new_things = [] #Список будет содержать полные записи новых вещей
    for i in range(len(loaded_things)):
        if (new_things_codes.count(loaded_things[i][0]) != 0):
            new_things.append(loaded_things[i])

    sqlRequests.addNewThings(new_things)

    return new_things


if HnMupd:
    def notify(new_things, type):
        print("Type: "+type+", Добавлено штук:"+str(len(new_things)))
        if len(new_things) != 0:
            notifier.sendMessageHnM(new_things, type)
    types = ['male','female','childrens','HOME']
    for i in range(len(types)):
        new_things = thingsUpdateHnM(types[i])
        notify(new_things, types[i])

