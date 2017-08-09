from time import sleep

import httpRequests
import sqlRequests
import telegramBot

def thingsUpdate():
    old_things = sqlRequests.getThings()
    print("Шмот из таблицы "+str(old_things))

    loaded_results = httpRequests.getThings()
    loaded_things = []
    loaded_things_codes = []
    for i in range(len(loaded_results)):
        result = (loaded_results[i]["defaultCode_string"],
                  loaded_results[i]["productWhitePrice_rub_double"],
                  loaded_results[i]["actualPrice_rub_double"],
                  loaded_results[i]["name_text_ru"],
                  loaded_results[i]["sizes_ru_string_mv"],)
        loaded_things.append(result)
        loaded_things_codes.append(result[0])
    print("Старые вещи: "+ str(len(old_things))+" шт.")
    print("Загружено: "+ str(len(loaded_things_codes))+" шт.")
    new_things_codes = list(set(loaded_things_codes).difference(old_things))
    print("Добавлено: "+ str(len(new_things_codes))+" шт.")
    new_things = []
    for i in range(len(loaded_things)):
        if (new_things_codes.count(loaded_things[i][0]) != 0):
            new_things.append(loaded_things[i])
    sqlRequests.addNewThings(new_things)

    return new_things


new_things = thingsUpdate()
if len(new_things) != 0:
    telegramBot.sendMessage(new_things)
