import requests
import json
import logging
import time
import sql_requests

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')
COMPANY = 'H&M'
PAGE_SIZE = 30

WOMAN_URL = 'https://app2.hm.com/hmwebservices/service/products/plp/hm-russia/Online/ru?q=:stock:category:ladies_all:sale:true&currentPage='
MEN_URL = 'https://app2.hm.com/hmwebservices/service/products/plp/hm-russia/Online/ru?q=:stock:category:men_all:sale:true&currentPage='
KIDS_URL = 'https://app2.hm.com/hmwebservices/service/products/plp/hm-russia/Online/ru?q=:stock:category:kids_all:sale:true&currentPage='
HOME_URL = 'https://app2.hm.com/hmwebservices/service/products/plp/hm-russia/Online/ru?q=:stock:category:home_all:sale:true&currentPage='
THING_BY_ID_URL = 'https://app2.hm.com/hmwebservices/service/article/get-article-by-code/hm-russia/Online/'
THING_URL = 'http://www2.hm.com'
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
    old_things = sql_requests.get_things(
        COMPANY)  # Подгружаем записаные в БД вещи, чтоб подгружать размер только для новых вещей
    try:
        while True:
            req = url + str(start_index) + '&pageSize=' + str(PAGE_SIZE)
            print(req)
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
                print("COMPANY: " + COMPANY + " | page: " + str(start_index + 1))
                start_index += 1
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
                code = full_result["articleCodes"][0]
                price = full_result['whitePrice'].get('value', 0)
                actual_price = full_result['redPrice'].get('value', 0)
                name = full_result['name']
                size = get_sizes(full_result['variantSizes'])
                link = THING_URL + full_result['linkPdp']
                if code not in old_things:
                    status = get_thing_status_by_id(code)
                    thing = [code, price, actual_price, name, size, link, status]
                else:
                    thing = [code, price, actual_price, name, size, link, True]
                results.append(thing)
            except ValueError as err:
                logging.error(u'' + str(err) + ' Ошибка парсинга: '+full_result)
        return results

def get_thing_status_by_id(thing_id):
    headers = sql_requests.get_headers(COMPANY)
    cookies = sql_requests.get_cookies(COMPANY)
    status = True
    try:
        req = THING_BY_ID_URL + str(thing_id) + "/ru"  # URL для API
        print(req)
        response = requests.get(req, headers=headers, cookies=cookies, timeout=15.0)
        if response.status_code == 200:
            cookies.update(dict(response.cookies))  # Обновляем куки
            sql_requests.set_cookies(COMPANY, str(cookies))  # Сохраняем обновленные куки в БД
            try:
                parsed_string = json.loads(response.content.decode('utf-8'))
                if parsed_string["product"].get("inStock", "False"):
                    status = True
                else:
                    status = False
            except KeyError as err:
                logging.error(u'' + str(err) + ' Ошибка парсинга JSON')
                status = False
        elif response.status_code == 404:
            status = False
    except requests.exceptions.ConnectTimeout as err:
        logging.error(u'' + str(err) + '')
    except requests.exceptions.ReadTimeout as err:
        logging.error(u'' + str(err) + '')
    except requests.exceptions.ConnectionError as err:
        logging.error(u'' + str(err) + '')
    except requests.exceptions.HTTPError as err:
        logging.error(u'' + str(err) + '')
    finally:
        return status

def get_sizes(sizes_list):
    sizes = []
    try:
        for size in sizes_list:
            sizes.append(size.get('filterCode', '-'))
    finally:
        return sizes


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