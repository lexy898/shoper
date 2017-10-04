from parsers import base_parser
from bs4 import BeautifulSoup
import json
import logging
from urllib.parse import unquote

class ParserNike(base_parser.BaseParser):
    def __init__(self):
        super().__init__()
        logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR,
                            filename=u'log.txt')
        self._PAGE_SIZE = 1
        self._START_INDEX = 1

        self._COMPANY = 'Nike'
        self._WOMAN_URL = 'https://store.nike.com/html-services/gridwallData?country=RU&lang_locale=ru_RU&gridwallPath=женщины-распродажа/47Z7pt&pn='
        self._MEN_URL = 'https://store.nike.com/html-services/gridwallData?country=RU&lang_locale=ru_RU&gridwallPath=мужчины-распродажа/47Z7pu&pn='
        self._BOYS_URL = 'https://store.nike.com/html-services/gridwallData?country=RU&lang_locale=ru_RU&gridwallPath=мальчики-распродажа/47Z7pv&pn='
        self._GIRLS_URL = 'https://store.nike.com/html-services/gridwallData?country=RU&lang_locale=ru_RU&gridwallPath=-/47Z7pw&pn='

        self._types_dict = {
            'woman': self._WOMAN_URL,
            'men': self._MEN_URL,
            'boys': self._BOYS_URL,
            'girls': self._GIRLS_URL
        }

    def _get_thing_status_by_page(self, thing_page):
        status = True
        try:
            if thing_page.status_code == 410:
                status = False
            elif thing_page.status_code == 200:
                soup = BeautifulSoup(thing_page.content, "html.parser")
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
        finally:
            return status

    def _create_req(self, url, start_index):
        req = url + str(start_index)
        return req

    def _get_things_by_sale_page(self, response, old_things):
        results = []
        try:
            parsed_string = json.loads(response.content.decode('utf-8'))
            if not parsed_string.get("sections"):
                return results
        except KeyError as err:
            logging.error(u'' + str(err) + ' Ошибка парсинга JSON')
            return results
        products = parsed_string['sections'][0]['products']
        for product in products:
            try:
                code = self._get_thing_code(product['pdpUrl'])
                price = self._format_price(product['overriddenLocalPrice'])
                actual_price = self._format_price(product['overriddenEmployeePrice'])
                name = product['subtitle'] + ' ' + product['title']
                link = unquote(product['pdpUrl'])
                if code not in old_things:
                    thing_page = self._get_thing_page(link)
                    size = self._get_sizes_by_page(thing_page)
                    status = self._get_thing_status_by_page(thing_page)
                else:
                    size = '-'
                    status = True
                results.append([code, price, actual_price, name, size, link, status])
            except ValueError as err:
                logging.error(u'' + str(err) + ' Ошибка парсинга: ' + product)
        return results

    def _get_sizes_by_page(self, thing_page):
        sizes = []
        try:
            if thing_page.status_code == 200:
                try:
                    soup = BeautifulSoup(thing_page.content, "html.parser")
                    sizes_list = soup.find('select', {'name': 'skuAndSize'}).find_all('option')
                    for size in sizes_list:
                        if not size.get('class'):
                            sizes.append(self._format_size(size.text))
                except AttributeError as err:
                    logging.error(u'' + str(err))
        finally:
            return sizes

    def _format_price(self, price):
        result = []
        try:
            for char in price:
                if char.isdigit():
                    result.append(char)
            return ''.join(result)
        except:
            return ''

    def _format_size(self, size):
        return size.replace('\n', '').replace('\t', '')

    def _get_thing_code(self, link):
        return link[link.rfind('pid'):]

    # Метод служит для вывода на экран текущей страницы, компании, типа вещей
    def _current_info(self, start_index):
        print("COMPANY: " + self._COMPANY + " | page: " + str(start_index))
