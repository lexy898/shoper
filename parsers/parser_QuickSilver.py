import requests
import logging
import sql_requests
import time
from bs4 import BeautifulSoup
import config

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR, filename=u'log.txt')
COMPANY = 'QuickSilver'
PAGE_SIZE = 48

MEN_URL = 'http://www.quiksilver.ru/skidki-men/'
KIDS_URL = 'http://www.quiksilver.ru/skidki-kids/'

def get_things(url):
    start_index = 0
    fail_counter = 0
    headers = sql_requests.get_headers(COMPANY)
    cookies = sql_requests.get_cookies(COMPANY)
    results = []
    old_things = sql_requests.get_things(COMPANY)  # Подгружаем записаные в БД вещи, чтоб подгружать размер только для новых вещей
    try:
        while True:
            print("COMPANY: " + COMPANY + " | page: " + str(start_index / PAGE_SIZE + 1))
            req = url+"?sz=48&start="+str(start_index)
            response = requests.get(req, headers=headers, cookies=cookies)
            if response.status_code == 200:
                cookies.update(dict(response.cookies))  # Обновляем куки
                soup = BeautifulSoup(response.content, "html.parser")

                product_grid = soup.find('div', class_='isproductgrid')
                products = product_grid.find_all('div', {'class': 'producttileinner'})
                if not products:
                    break
                for product in products:
                    code = product.find('div', {'class': 'image thumbnail productimage'}).get('data-productid')
                    price = product.find('div', {'class': 'pricinginitial'}).find('div').find('div').get('data-standardprice').replace("-","0")
                    actual_price = product.find('div', {'class': 'pricinginitial'}).find('div').find('div').get('data-salesprice').replace("-","0")
                    name = product.find('div', {'class': 'name'}).find('a').text
                    link = product.find('div', {'class': 'name'}).find('a').get('href')
                    if code not in old_things:
                        thing = [code, price, actual_price, name, get_sizes(link), link]
                    else:
                        thing = [code, price, actual_price, name, '-', link]
                    results.append(thing)
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

def get_thing_status_by_id(thing_id):
    headers = sql_requests.get_headers(COMPANY)
    cookies = sql_requests.get_cookies(COMPANY)
    status = True
    try:
        response = requests.get(sql_requests.get_link_by_id(thing_id), headers=headers, cookies=cookies, timeout=15.0)
        if response.status_code == 200:
            cookies.update(dict(response.cookies))  # Обновляем куки
            sql_requests.set_cookies(COMPANY, str(cookies))  # Сохраняем обновленные куки в БД
            try:
                BeautifulSoup(response.content, "html.parser").find('div', {'class': 'promoprice'}).text
            except:
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

def get_sizes(link):
    headers = sql_requests.get_headers(COMPANY)
    cookies = sql_requests.get_cookies(COMPANY)
    sizes = []
    try:
        response = requests.get(link, headers=headers, cookies=cookies, timeout=15.0)
        if response.status_code == 200:
            cookies.update(dict(response.cookies))  # Обновляем куки
            sql_requests.set_cookies(COMPANY, str(cookies))  # Сохраняем обновленные куки в БД
            try:
                soup = BeautifulSoup(response.content, "html.parser")
                swatchesdisplay = soup.find('div', {'class': 'sizes-panel-inner'}).find('ul', {'class': 'swatchesdisplay'})
                sizes_list = swatchesdisplay.find_all('li')
                for size in sizes_list:
                    if 'variant-off' in size.get('class') or 'master-off' in size.get('class'):
                        continue
                    else:
                        sizes.append(size.find('a').text)
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

def get_QuickSilver_loaded_results(type):
    if type == 'men':
        return get_things(MEN_URL)
    elif type == 'kids':
        return get_things(KIDS_URL)
    else:
        print("Параметра " + str(type) + " не существует")
        return 0
