from parsers import base_parser
import requests
import json
import logging
import sql_requests
import config

class ParserHnM(base_parser.BaseParser):
    def __init__(self):
        super().__init__()
        logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR,
                            filename=u'log.txt')
        self._PAGE_SIZE = 30
        self._COMPANY = 'H&M'

        self._WOMAN_URL = 'https://app2.hm.com/hmwebservices/service/products/plp/hm-russia/Online/ru?q=:stock:category:ladies_all:sale:true&currentPage='
        self._MEN_URL = 'https://app2.hm.com/hmwebservices/service/products/plp/hm-russia/Online/ru?q=:stock:category:men_all:sale:true&currentPage='
        self._KIDS_URL = 'https://app2.hm.com/hmwebservices/service/products/plp/hm-russia/Online/ru?q=:stock:category:kids_all:sale:true&currentPage='
        self._HOME_URL = 'https://app2.hm.com/hmwebservices/service/products/plp/hm-russia/Online/ru?q=:stock:category:home_all:sale:true&currentPage='

        self._THING_BY_ID_URL = 'https://app2.hm.com/hmwebservices/service/article/get-article-by-code/hm-russia/Online/'
        self._THING_URL = 'http://www2.hm.com'

        self._types_dict = {
            'woman': self._WOMAN_URL,
            'men': self._MEN_URL,
            'kids': self._KIDS_URL,
            'home': self._HOME_URL
        }

    def _get_thing_status_by_page(self, thing_page):
        status = True
        try:
            if thing_page.status_code == 200:
                try:
                    parsed_string = json.loads(thing_page.content.decode('utf-8'))
                    if parsed_string["product"].get("inStock", "False"):
                        status = True
                    else:
                        status = False
                except KeyError as err:
                    logging.error(u'' + str(err) + ' Ошибка парсинга JSON')
                    status = False
            elif thing_page.status_code == 404:
                status = False
        finally:
            return status

    def _get_thing_page(self, thing_id):
        headers = sql_requests.get_headers(self._COMPANY)
        cookies = sql_requests.get_cookies(self._COMPANY)
        try:
            req = self._THING_BY_ID_URL + str(thing_id) + "/ru"  # URL для API
            print(req)
            response = requests.get(req, headers=headers, cookies=cookies, timeout=config.get_timeout())
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
        thing_page = self._get_thing_page(thing_id)
        return self._get_thing_status_by_page(thing_page)

    def _get_things_by_sale_page(self, response, old_things):
        results = []
        try:
            parsed_string = json.loads(response.content.decode('utf-8'))
            if not parsed_string["results"]:
                return results
        except ValueError as err:
            logging.error(u'' + str(err) + ' Ошибка парсинга JSON')
            return results
        products = parsed_string["results"]
        for product in products:
            try:
                code = product["articleCodes"][0]
                price = product['whitePrice'].get('value', 0)
                actual_price = product['redPrice'].get('value', 0)
                name = product['name']
                size = self._get_sizes(product['variantSizes'])
                link = self._THING_URL + product['linkPdp']
                if code not in old_things:
                    status = self.get_thing_status_by_id(code)
                    thing = [code, price, actual_price, name, size, link, status]
                else:
                    thing = [code, price, actual_price, name, size, link, True]
                results.append(thing)
            except ValueError as err:
                logging.error(u'' + str(err) + ' Ошибка парсинга: ' + product)
        return results

    def _create_req(self, url, start_index):
        req = url + str(start_index) + '&pageSize=' + str(self._PAGE_SIZE)
        return req

    def _get_sizes(self, sizes_list):
        sizes = []
        try:
            for size in sizes_list:
                sizes.append(size.get('filterCode', '-'))
        finally:
            return sizes

    def _increment_start_index(self, start_index):
        return start_index + 1

    def _current_info(self, start_index):
        print("COMPANY: " + self._COMPANY + " | page: " + str(start_index+1))