from parsers import base_parser
from bs4 import BeautifulSoup
import logging


class ParserAdidas(base_parser.BaseParser):
    def __init__(self):
        super().__init__()
        logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.ERROR,
                            filename=u'log.txt')
        self._PAGE_SIZE = 120
        self._COMPANY = 'Adidas'

        self._MEN_URL = 'http://www.adidas.ru/muzhchiny-rasprodazha'
        self._WOMAN_URL = 'http://www.adidas.ru/zhenschiny-rasprodazha'
        self._KIDS_URL = 'http://www.adidas.ru/deti-rasprodazha'

        self._types_dict = {
            'men': self._MEN_URL,
            'woman': self._WOMAN_URL,
            'kids': self._KIDS_URL
        }

    def _get_thing_status_by_page(self, thing_page):
        status = True
        try:
            if thing_page.status_code == 200:
                try:
                    soup = BeautifulSoup(thing_page.content, "html.parser")
                    soup.find('span', {'class': 'sale-price discounted'}).get('data-sale-price')
                except AttributeError:
                    status = False
        finally:
            return status

    def _create_req(self, url, start_index):
        req = url + '?sz=' + str(self._PAGE_SIZE) + '&start=' + str(start_index)
        return req

    def _get_things_by_sale_page(self, response, old_things):
        results = []
        soup = BeautifulSoup(response.content, "html.parser")
        products = soup.find('div', {'id': 'hc-container'}).find_all('div', {'class': 'product-tile'})
        if not products:
            return results
        for product in products:
            try:
                if 'Распродан' not in product.find('span', {'class': 'badge-text'}).text:
                    prod_info = product.find('div', {'class', 'product-info-wrapper stack track'})
                    code = prod_info.find('div', {'class': 'product-info-inner-content clearfix with-badges'}) \
                        .find('a').get('data-track')
                    price = self._format_price(prod_info.find('span', {'class', 'baseprice'}).text)
                    actual_price = self._format_price(prod_info.find('span', {'class', 'salesprice discount-price'}).text)
                    name = prod_info.find('div', {'class': 'product-info-inner-content clearfix with-badges'}) \
                        .find('a').find('span', {'class': 'title'}).text
                    link = prod_info.find('div', {'class': 'product-info-inner-content clearfix with-badges'}) \
                        .find('a').get('href')
                    if code not in old_things:
                        thing_page = self._get_thing_page(link)
                        size = self._get_sizes_by_page(thing_page)
                        status = self._get_thing_status_by_page(thing_page)
                    else:
                        size = '-'
                        status = True
                    results.append([code, price, actual_price, name, size, link, status])
            except ValueError as err:
                logging.error(u'' + str(err) + '')
                continue
            except AttributeError:
                continue
        return results

    def _get_sizes_by_page(self, thing_page):
        sizes = []
        try:
            if thing_page.status_code == 200:
                try:
                    soup = BeautifulSoup(thing_page.content, "html.parser")
                    sizes_list = soup.find('ispagecontextset', {'name': 'product_size*'}).find_all('option')
                    for size in sizes_list:
                        sizes.append(self._format_size(size.text))
                except ValueError as err:
                    logging.error(u'' + str(err) + ' Ошибка парсинга HTML')
        finally:
            return sizes

    def _format_price(self, price):
        result = []
        for char in price:
            if char.isdigit():
                result.append(char)
        return ''.join(result)

    def _format_size(self, size):
        return size.replace('\n', '').replace('\t', '')
