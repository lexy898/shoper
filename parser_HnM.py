import requests
import json
import logging
import time
import sql_requests

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')
COMPANY = 'H&M'
PAGE_SIZE = 30

WOMAN_URL = 'https://app2.hm.com/hmwebservices/service/app/productList?storeId=hm-russia&catalogVersion=Online&locale=ru&categories=ladies_all&start='
MEN_URL = 'https://app2.hm.com/hmwebservices/service/app/productList?storeId=hm-russia&catalogVersion=Online&locale=ru&categories=men_all&start='
KIDS_URL = 'https://app2.hm.com/hmwebservices/service/app/productList?storeId=hm-russia&catalogVersion=Online&locale=ru&categories=kids_all&start='
HOME_URL = 'https://app2.hm.com/hmwebservices/service/app/productList?storeId=hm-russia&catalogVersion=Online&locale=ru&categories=home_all&start='
END_OF_URL = '&pageSize=30&sale_boolean=true'
THING_BY_ID_URL = 'https://app2.hm.com/hmwebservices/service/article/get-article-by-code/hm-russia/Online/'
'''
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
'''

def get_things(url):
    global parsed_string
    start_index = 0
    fail_counter = 0
    loaded_results = []
    results = []
    headers = sql_requests.get_headers(COMPANY)
    cookies = sql_requests.get_cookies(COMPANY)
    try:
        while True:
            req = url + str(start_index) + END_OF_URL
            response = requests.get(req, headers=headers, cookies=cookies)
            if response.status_code == 200:
                cookies.update(dict(response.cookies)) #Обновляем куки
                try:
                    parsed_string = json.loads(response.content.decode('utf-8'))
                    if not parsed_string["results"]:
                        break
                except ValueError as err:
                    logging.error(u'' + str(err) + ' Ошибка парсинга JSON')
                    break
                loaded_results.extend(parsed_string["results"])
                print("COMPANY: " + COMPANY + " | page: " + str(start_index / PAGE_SIZE + 1))
                start_index += PAGE_SIZE
                fail_counter = 0
            else:
                if response.status_code == 403 and fail_counter < 5:
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
    finally:
        for full_result in loaded_results:
            try:
                result = [full_result["defaultCode_string"],
                          full_result.get("productWhitePrice_rub_double", 0),
                          full_result.get("actualPrice_rub_double", 0),
                          full_result["name_text_ru"],
                          full_result.get("sizes_ru_string_mv", "-"), ]
                results.append(result)
            except ValueError as err:
                logging.error(u'' + str(err) + ' Ошибка парсинга: '+full_result)
        return results

def get_thing_status_by_id(id):
    global parsed_string
    headers = sql_requests.get_headers(COMPANY)
    cookies = sql_requests.get_cookies(COMPANY)
    try:
        req = THING_BY_ID_URL + str(id) + "/ru"
        response = requests.get(req, headers=headers, cookies=cookies, timeout=15.0)
        if response.status_code == 200:
            cookies.update(dict(response.cookies))  # Обновляем куки
            sql_requests.set_cookies(COMPANY, str(cookies))  # Сохраняем обновленные куки в БД
            try:
                parsed_string = json.loads(response.content.decode('utf-8'))
                if not parsed_string["product"]:
                    return False
            except ValueError as err:
                logging.error(u'' + str(err) + ' Ошибка парсинга JSON')
            product = parsed_string["product"]
            inStock = product.get("inStock", "False")
            print("id: "+str(id)+" inStock: "+str(inStock))
            if inStock:
                return True
            else:
                return False

    except requests.exceptions.ConnectTimeout as err:
        logging.error(u'' + str(err) + '')
        return False
    except requests.exceptions.ReadTimeout as err:
        logging.error(u'' + str(err) + '')
        return False
    except requests.exceptions.ConnectionError as err:
        logging.error(u'' + str(err) + '')
        return False
    except requests.exceptions.HTTPError as err:
        logging.error(u'' + str(err) + '')
        return False

def get_HnM_loaded_results(type):
    if type == 'men':
        return get_things(MEN_URL)
    elif type == 'woman':
        return get_things(WOMAN_URL)
    elif type == 'kids':
        return get_things(KIDS_URL)
    elif type == 'home':
        return get_things(HOME_URL)
    else:
        print("Параметра " + str(type) + " не существует")
        return 0
