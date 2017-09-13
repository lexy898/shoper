import requests
import logging
import sql_requests
import time
import json


logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')
COMPANY = 'MANGO'
PAGE_SIZE = 1

WOMAN_URL = "http://shop.mango.com/services/productlist/products/RU/she/sections_she_RU_resto_PromoSeptiembreRU.january_she/?pageNum="
MEN_URL = "http://shop.mango.com/services/productlist/products/RU/he/sections_he_RU_PromoSeptiembreRU.january_he/?pageNum="
BOYS_URL = "http://shop.mango.com/services/cataloglist/filtersProducts/RU/nino/sections_kidsO_RU_PromoSeptiembreRU.january_kidsO/?pageNum="
BOYS_KIDS_URL= "http://shop.mango.com/services/cataloglist/filtersProducts/RU/nino/sections_babyNino_RU_PromoSeptiembreRU.january_baby/?pageNum="
GIRLS_URL = "http://shop.mango.com/services/cataloglist/filtersProducts/RU/nina/sections_kidsA_RU_new_PromoSeptiembreRU.january_kidsA/?pageNum="
GIRLS_KIDS_URL = "http://shop.mango.com/services/cataloglist/filtersProducts/RU/nina/sections_babyNina_RU_new_PromoSeptiembreRU.january_baby/?pageNum="
VIOLETA_URL = "http://shop.mango.com/services/cataloglist/filtersProducts/RU/violeta/sections_violeta_RU_PromoSeptiembreRU.january_violeta/?pageNum="
END_OF_URL = "&rowsPerPage=20&columnsPerRow=2"

def get_things(url, END_OF_URL):
    global parsed_string
    start_index = 1
    fail_counter = 0
    loaded_results = []
    results = []
    headers = sql_requests.get_headers(COMPANY)
    cookies = sql_requests.get_cookies(COMPANY)
    try:
        while True:
            req = url + str(start_index) + END_OF_URL
            print(req)
            response = requests.get(req, headers=headers, cookies=cookies)
            if (response.status_code == 200):
                cookies.update(dict(response.cookies)) #Обновляем куки
                json_string = response.content
                try:
                    parsed_string = json.loads(json_string)
                    print(parsed_string["groups"])
                    if (parsed_string["groups"] == []):
                        break
                except ValueError as err:
                    logging.error(u'' + str(err) + ' Ошибка парсинга JSON')
                    break
                loaded_results.extend(parsed_string["garments"])
                print("COMPANY: " + COMPANY + " | page: " + str(start_index / PAGE_SIZE + 1))
                start_index += PAGE_SIZE
                fail_counter = 0
            else:
                if (response.status_code == 403 and fail_counter < 5):
                    print(response.status_code)
                    fail_counter += 1
                    time.sleep(10)
                else:
                    break
        sql_requests.set_cookies(COMPANY, str(cookies)) #Сохраняем обновленные куки в БД

    except requests.exceptions.ConnectTimeout as err:
        logging.error(u'' + str(err) + '')
    except requests.exceptions.ReadTimeout as err:
        logging.error(u'' + str(err) + '')
    except requests.exceptions.ConnectionError as err:
        logging.error(u'' + str(err) + '')
    except requests.exceptions.HTTPError as err:
        logging.error(u'' + str(err) + '')

    for full_result in loaded_results:
        try:
            result = [full_result["garmentId"],
                      full_result.get("crossedOutPrices",0),
                      full_result.get("salePrice",0),
                      full_result["shortDescription"],]
            results.append(result)
        except ValueError as err:
            logging.error(u'' + str(err) + ' Ошибка парсинга: '+full_result)
    return results

def get_thing_status_by_id(id):
    return True

def get_mango_loaded_results(type):
    if type == 'woman':
        return get_things(WOMAN_URL, END_OF_URL)
    elif type == 'men':
        return get_things(WOMAN_URL, END_OF_URL)
    elif type == 'girls':
        return get_things(WOMAN_URL, END_OF_URL)
    elif type == 'girls_kids':
        return get_things(WOMAN_URL, END_OF_URL)
    elif type == 'boys':
        return get_things(WOMAN_URL, END_OF_URL)
    elif type == 'boys_kids':
        return get_things(WOMAN_URL, END_OF_URL)
    elif type == 'violeta':
        return get_things(WOMAN_URL, END_OF_URL)
    else:
        print("Параметра " + str(type) + " не существует")
        return 0

get_mango_loaded_results('woman')