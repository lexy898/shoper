import requests
import json
import logging
import time
import sql_requests
from bs4 import BeautifulSoup

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')
COMPANY = 'Nike'
PAGE_SIZE = 1

WOMAN_URL = 'https://store.nike.com/html-services/gridwallData?country=RU&lang_locale=ru_RU&gridwallPath=женщины-распродажа/47Z7pt&pn='
MEN_URL = 'https://store.nike.com/html-services/gridwallData?country=RU&lang_locale=ru_RU&gridwallPath=мужчины-распродажа/47Z7pu&pn='
BOYS_URL = 'https://store.nike.com/html-services/gridwallData?country=RU&lang_locale=ru_RU&gridwallPath=мальчики-распродажа/47Z7pv&pn='
GIRLS_URL = 'https://store.nike.com/html-services/gridwallData?country=RU&lang_locale=ru_RU&gridwallPath=-/47Z7pw&pn='


def get_things(url):
    start_index = 1
    fail_counter = 0
    loaded_results = []
    results = []
    headers = sql_requests.get_headers(COMPANY)
    cookies = sql_requests.get_cookies(COMPANY)
    old_things = sql_requests.get_things(
        COMPANY)  # Подгружаем записаные в БД вещи, чтоб подгружать размер только для новых вещей
    try:
        while True:
            req = url + str(start_index)
            response = requests.get(req, headers=headers, cookies=cookies)
            if response.status_code == 200:
                cookies.update(dict(response.cookies))  # Обновляем куки
                try:
                    parsed_string = json.loads(response.content.decode('utf-8'))
                    if not parsed_string.get("sections"):
                        break
                except KeyError as err:
                    logging.error(u'' + str(err) + ' Ошибка парсинга JSON')
                    break
                loaded_results.extend(parsed_string['sections'][0]['products'])
                print("COMPANY: " + COMPANY + " | page: " + str(start_index / PAGE_SIZE))
                start_index += PAGE_SIZE
                fail_counter = 0
            else:
                if response.status_code == 403 and fail_counter < 5:
                    print(response.status_code)
                    fail_counter += 1
                    time.sleep(10)
                else:
                    break
        sql_requests.set_cookies(COMPANY, str(cookies))  # Сохраняем обновленные куки в БД

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
                code = get_thing_code(full_result['pdpUrl'])
                price = format_price(full_result['overriddenLocalPrice'])
                actual_price = format_price(full_result['overriddenEmployeePrice'])
                name = full_result['subtitle'] + ' ' + full_result['title']
                link = full_result['pdpUrl']
                if code not in old_things:
                    size = get_sizes(link)
                else:
                    size = '-'
                results.append([code, price, actual_price, name, size, link])
            except ValueError as err:
                logging.error(u'' + str(err) + ' Ошибка парсинга: ' + full_result)
        return results


def get_sizes(link):
    headers = sql_requests.get_headers(COMPANY)
    cookies = sql_requests.get_cookies(COMPANY)
    sizes = []
    try:
        print(link)
        response = requests.get(link, headers=headers, cookies=cookies, timeout=15.0)
        if response.status_code == 200:
            cookies.update(dict(response.cookies))  # Обновляем куки
            sql_requests.set_cookies(COMPANY, str(cookies))  # Сохраняем обновленные куки в БД
            try:
                soup = BeautifulSoup(response.content, "html.parser")
                sizes_list = soup.find('select', {'name': 'skuAndSize'}).find_all('option')
                for size in sizes_list:
                    if not size.get('class'):
                        sizes.append(format_size(size.text))
            except AttributeError as err:
                logging.error(u'' + str(err))
    except requests.exceptions.ConnectTimeout as err:
        logging.error(u'' + str(err) + '')
    except requests.exceptions.ReadTimeout as err:
        logging.error(u'' + str(err) + '')
    except requests.exceptions.ConnectionError as err:
        logging.error(u'' + str(err) + '')
    except requests.exceptions.HTTPError as err:
        logging.error(u'' + str(err) + '')
    finally:
        return sizes


def get_thing_code(link):
    return link[link.rfind('pid'):]


def format_price(price):
    result = []
    try:
        for char in price:
            if char.isdigit():
                result.append(char)
        return ''.join(result)
    except:
        return ''


def format_size(size):
    return size.replace('\n', '').replace('\t', '').replace(' ', '')


def get_thing_status_by_id(thing_id):
    headers = sql_requests.get_headers(COMPANY)
    cookies = sql_requests.get_cookies(COMPANY)
    status = True
    try:
        print(sql_requests.get_link_by_id(thing_id))
        response = requests.get(sql_requests.get_link_by_id(thing_id), headers=headers, cookies=cookies, timeout=15.0)
        if response.status_code == 410:
            status = False
        elif response.status_code == 200:
            cookies.update(dict(response.cookies))  # Обновляем куки
            sql_requests.set_cookies(COMPANY, str(cookies))  # Сохраняем обновленные куки в БД
            soup = BeautifulSoup(response.content, "html.parser")
            '''
            Если отсутствует элемент "НЕТ В НАЛИЧИИ", то проверяется наличие элемента скидочной цены
            '''
            if not soup.find('div', {'class': 'exp-pdp-nostock-text'}):
                try:
                    soup.find('span', {'class': 'exp-pdp-overridden-local-price'}).text
                except AttributeError:
                    status = False
            else:
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


def get_Nike_loaded_results(type):
    if type == 'men':
        return get_things(MEN_URL)
    elif type == 'woman':
        return get_things(WOMAN_URL)
    elif type == 'boys':
        return get_things(BOYS_URL)
    elif type == 'girls':
        return get_things(GIRLS_URL)
    else:
        print("Параметра " + str(type) + " не существует")
        return 0
