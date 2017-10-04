import requests
import logging
import sql_requests
import config

class BaseParser:

    def __init__(self):
        logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR,
                                           filename=u'log.txt')
        self._COMPANY = 'Company'
        self._PAGE_SIZE = 1
        self._START_INDEX = 0
        self._types_dict = {}

    # Метод для получения всех загруженных вещей всех имеющихся типов
    def get_loaded_results(self):
        loaded_results = []
        for key in self._types_dict:
            print('TYPE: '+key)
            loaded_results.extend(self.get_things(self._types_dict.get(key)))

    def _get_thing_page(self, link):
        headers = sql_requests.get_headers(self._COMPANY)
        cookies = sql_requests.get_cookies(self._COMPANY)
        try:
            print(link)
            response = requests.get(link, headers=headers, cookies=cookies, timeout=config.get_timeout())
            if response.status_code == 200:
                cookies.update(dict(response.cookies))  # Обновляем куки
                sql_requests.set_cookies(self._COMPANY, str(cookies))  # Сохраняем обновленные куки в БД
            return response
        except requests.exceptions.ConnectTimeout as err:
            logging.error(u'' + str(err) + '')
        except requests.exceptions.ReadTimeout as err:
            logging.error(u'' + str(err) + '')
        except requests.exceptions.ConnectionError as err:
            logging.error(u'' + str(err) + '')
        except requests.exceptions.HTTPError as err:
            logging.error(u'' + str(err) + '')

    def get_thing_status_by_id(self, thing_id):
        thing_page = self._get_thing_page(sql_requests.get_link_by_id(thing_id))
        return self._get_thing_status_by_page(thing_page)

    def _get_thing_status_by_page(self, thing_page):
        return True

    def get_things(self, url):
        start_index = self._START_INDEX
        headers = sql_requests.get_headers(self._COMPANY)
        cookies = sql_requests.get_cookies(self._COMPANY)
        results = []
        # Получаем записаные в БД вещи, чтоб подгружать потом статус и размер только новых вещей
        old_things = sql_requests.get_things(self._COMPANY)
        try:
            while True:
                self._current_info(start_index)
                req = self._create_req(url, start_index)
                print(req)
                response = requests.get(req, headers=headers, cookies=cookies, timeout=config.get_timeout())
                if response.status_code == 200:
                    cookies.update(dict(response.cookies))  # Обновляем куки
                    things = self._get_things_by_sale_page(response, old_things)
                    if not things:
                        break
                    results.extend(things)
                sql_requests.set_cookies(self._COMPANY, str(cookies))  # Сохраняем обновленные куки в БД
                start_index += self._PAGE_SIZE
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

    def _create_req(self, url, start_index):
        return url

    # Метод служит для получения вещей со странички сайта в разделе скидки
    def _get_things_by_sale_page(self, response, old_things):
        return []

    # Метод служит для вывода на экран текущей страницы, компании, типа вещей
    def _current_info(self, start_index):
        print("COMPANY: " + self._COMPANY + " | page: " + str(start_index / self._PAGE_SIZE + 1))
