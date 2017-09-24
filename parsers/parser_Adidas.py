import requests
import logging
import sql_requests
import time
from bs4 import BeautifulSoup
import config

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')
COMPANY = 'Adidas'
PAGE_SIZE = 120

MEN_URL = 'http://www.adidas.ru/muzhchiny-rasprodazha'
WOMAN_URL = 'http://www.adidas.ru/zhenschiny-rasprodazha'
KIDS_URL = 'http://www.adidas.ru/deti-rasprodazha'
THING_BY_ID_URL = config.get_product_page(COMPANY)


def get_things(url):
    start_index = 0
    fail_counter = 0
    headers = sql_requests.get_headers(COMPANY)
    cookies = sql_requests.get_cookies(COMPANY)
    results = []
    old_things = sql_requests.get_things(
        COMPANY)  # Подгружаем записаные в БД вещи, чтоб подгружать размер только для новых вещей
    try:
        while True:
            print('COMPANY: ' + COMPANY + ' | page: ' + str(start_index / PAGE_SIZE + 1))
            req = url + '?sz=' + str(PAGE_SIZE) + '&start=' + str(start_index)
            response = requests.get(req, headers=headers, cookies=cookies)
            if response.status_code == 200:
                cookies.update(dict(response.cookies))  # Обновляем куки
                soup = BeautifulSoup(response.content, "html.parser")
                products = soup.find('div', {'id': 'hc-container'}).find_all('div', {'class': 'product-tile'})
                if not products:
                    break
                for product in products:
                    if 'Распродан' not in product.find('span', {'class': 'badge-text'}).text:
                        try:
                            prod_info = product.find('div', {'class', 'product-info-wrapper stack track'})
                            code = prod_info.find('div', {'class': 'product-info-inner-content clearfix with-badges'}) \
                                .find('a').get('data-track')
                            price = format_price(prod_info.find('span', {'class', 'baseprice'}).text)
                            actual_price = format_price(prod_info.find('span', {'class', 'salesprice discount-price'}).text)
                            name = prod_info.find('div', {'class': 'product-info-inner-content clearfix with-badges'}) \
                                .find('a').find('span', {'class': 'title'}).text
                            if code not in old_things:
                                thing = [code, price, actual_price, name, get_sizes(code)]
                            else:
                                thing = [code, price, actual_price, name, '-']
                            results.append(thing)
                        except:
                            continue
            else:
                if response.status_code == 403 and fail_counter < 5:
                    print(response.status_code)
                    fail_counter += 1
                    time.sleep(10)
                else:
                    break
            sql_requests.set_cookies(COMPANY, str(cookies))  # Сохраняем обновленные куки в БД
            fail_counter = 0
            start_index += PAGE_SIZE
    except requests.exceptions.ConnectTimeout as err:
        logging.error(u'' + str(err) + '')
    except requests.exceptions.ReadTimeout as err:
        logging.error(u'' + str(err) + '')
    except requests.exceptions.ConnectionError as err:
        logging.error(u'' + str(err) + '')
    except requests.exceptions.HTTPError as err:
        logging.error(u'' + str(err) + '')
    finally:
        print("Вещей загружено: " + str(len(results)))
        return results


def format_price(price):
    result = []
    for char in price:
        if char.isdigit():
            result.append(char)
    return ''.join(result)


def format_size(size):
    return size.replace('\n', '').replace('\t', '')


def get_sizes(good_id):
    headers = sql_requests.get_headers(COMPANY)
    cookies = sql_requests.get_cookies(COMPANY)
    sizes = []
    try:
        req = THING_BY_ID_URL + str(good_id) + ".html"
        print(req)
        response = requests.get(req, headers=headers, cookies=cookies, timeout=15.0)
        if response.status_code == 200:
            cookies.update(dict(response.cookies))  # Обновляем куки
            sql_requests.set_cookies(COMPANY, str(cookies))  # Сохраняем обновленные куки в БД
            try:
                soup = BeautifulSoup(response.content, "html.parser")
                sizes_list = soup.find('ispagecontextset', {'name': 'product_size*'}).find_all('option')
                for size in sizes_list:
                    sizes.append(format_size(size.text))
            except ValueError as err:
                logging.error(u'' + str(err) + ' Ошибка парсинга HTML')
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


def get_thing_status_by_id(id):
    return True


def get_Adidas_loaded_results(type):
    if type == 'woman':
        return get_things(WOMAN_URL)
    elif type == 'kids':
        return get_things(KIDS_URL)
    elif type == 'men':
        return get_things(MEN_URL)
    else:
        print("Параметра " + str(type) + " не существует")
        return 0